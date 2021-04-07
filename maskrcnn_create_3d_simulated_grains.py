import numpy as np
import cv2
import os
import math
import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import pickle
import sys
import json


class GrainGenator:
    def __init__(self):
        self.output_dir = ""
        self.id_dataset = 0
        self.n_tracks = [80, 80]
        self.param_minimum_distance = 0.2 # micron    
        self.n_pixel_original = 2048
        self.n_divide = 8
        self.n_view = 1
        self.track_ranges_micron = [2.6, 5.2]
        self.sigma_track_range = 0.7 #micron
        self.distance_between_AgBr = 0.05 # this value is not accurate
        self.view_margin = 0.5 # micron
        self.n_noises_loc = 3
        self.n_noises_scale = 1
        self.n_max_grain_in_cluster = 5
        self.sigma_grain_in_cluster = 0.1
        self.thickness_boron = 0.200 # ~200nm
        self.thickness_protection = 0.060 # 2V101501, NiC:46nm + C:14nm
        self.thickness_noise = 0.008
        self.threshold_z = 0.3
        self.probability_development = [0.08, 0.15]
        self.max_slope = 0.00
        self.calc_secondary_parameters()

        self.list_view_track_grain = []
        self.list_generated_range = []
        self.list_xyz = []

    def calc_secondary_parameters(self):
        self.n_pixel = int(self.n_pixel_original / self.n_divide)
        self.view_size = 50 / 909 * self.n_pixel # 50micron=909pix
        self.depth_boron = self.thickness_boron + self.thickness_protection

    def load_parameters_from_json(self, jsonname):
        with open(jsonname) as f:
            params = json.load(f)
        for key, val in params.items():
            self.__dict__[key] = val
        self.calc_secondary_parameters()    
        return

    def create_output_dir(self):
        self.int_param_minimum_distance = int(self.param_minimum_distance * 100)    
        self.output_dir = f"dist{self.int_param_minimum_distance:03d}_t{self.n_tracks[0]:03d}_t{self.n_tracks[0]:03d}_{self.id_dataset:02d}"
        os.makedirs(f"{self.output_dir}", exist_ok=True)

    def get_root_point(self):
        root_x = np.random.uniform(0, self.view_size)
        root_y = np.random.uniform(0, self.view_size)
        root_z = np.random.uniform(-self.depth_boron, -self.thickness_protection)
        return root_x, root_y, root_z

    def generate_tracks_and_noises(self):
        self.n_image = self.n_view * self.n_divide * self.n_divide
        for i in range(self.n_image):
            print(f"view {i} in {self.n_image}")
            slope_dzdx = np.random.uniform(0, self.max_slope)
            slope_dzdy = np.random.uniform(0, self.max_slope)
            list_track_grain = []
            self.generate_tracks(list_track_grain, slope_dzdx, slope_dzdy)
            self.generate_noises(list_track_grain, slope_dzdx, slope_dzdy)
            self.list_view_track_grain.append(list_track_grain)

    def generate_tracks(self, list_track_grain, slope_dzdx, slope_dzdy):
        list_boundary_point = []
        n_track_in_this_image = np.random.uniform(self.n_tracks[0], self.n_tracks[1])
        probability_development_in_this_image = np.random.uniform(self.probability_development[0], self.probability_development[1])
        while len(list_track_grain) < n_track_in_this_image:
            xyz = create_uniform_sphere_xyz()
            xyz[2] = abs(xyz[2]) # z > 0
            track_range = random.choice(self.track_ranges_micron)
            track_range += random.gauss(0, self.sigma_track_range)
            #
            root_x = np.random.uniform(0, self.view_size)
            root_y = np.random.uniform(0, self.view_size)
            root_z = np.random.uniform(-self.depth_boron, -self.thickness_protection)
            #
            step = 0.0
            list_grain = []
            while step < track_range:
                this_x = root_x +  xyz[0] * step
                this_y = root_y +  xyz[1] * step
                this_z = root_z +  xyz[2] * step
                if np.random.uniform(0, 1) < probability_development_in_this_image:
                    if  this_z > 0.0: # in emulsion layer
                        this_z += root_x * slope_dzdx + root_y * slope_dzdy
                        list_grain.append((this_x, this_y, this_z))
                step += self.distance_between_AgBr
            # end of loop for a track
            if len(list_grain) == 0:
                continue
            first_grain = list_grain[0]
            last_grain = list_grain[-1]
            if first_grain[0] < 0 + self.view_margin or self.view_size - self.view_margin < first_grain[0]:
                continue # because this point is out of effective X
            if first_grain[1] < 0 + self.view_margin or self.view_size - self.view_margin < first_grain[1]:
                continue # because this point is out of effective Y
            if last_grain[2] < self.threshold_z:
                continue
            #
            min_dist = 9999.9
            for b in list_boundary_point:
                this_distance = math.hypot(b[0] - first_grain[0], b[1] - first_grain[1])
                min_dist = this_distance if this_distance < min_dist else min_dist
            if min_dist < self.param_minimum_distance:
                continue # because too close
            #
            list_boundary_point.append(first_grain)
            list_track_grain.append({"type":"t", "list_grain":list_grain, "root":[root_x, root_y, root_z]})
            self.list_xyz.append(xyz)
            self.list_generated_range.append(track_range)

    def generate_noises(self, list_track_grain, slope_dzdx, slope_dzdy):
        n_noises = np.random.normal(loc = self.n_noises_loc, scale = self.n_noises_scale)
        n_noises = int(n_noises)
        for _ in range(n_noises):
            n_cluster = int( random.uniform(1, self.n_max_grain_in_cluster))
            root_x = np.random.uniform(0, self.view_size)
            root_y = np.random.uniform(0, self.view_size)
            root_z = np.random.uniform(0, self.thickness_noise)
            list_grain_noise = []
            for _ in range(n_cluster):
                this_x = root_x + np.random.normal(loc = 0, scale = self.sigma_grain_in_cluster)
                this_y = root_y + np.random.normal(loc = 0, scale = self.sigma_grain_in_cluster)
                this_z = root_z + np.random.normal(loc = 0, scale = self.sigma_grain_in_cluster)
                this_z += root_x * slope_dzdx + root_y * slope_dzdy
                list_grain_noise.append((this_x, this_y, this_z))
            list_track_grain.append({"type":"n","list_grain":list_grain_noise})

    def dump_pickle_file(self, pickle_name="grains.pickle"):
        with open(f"{self.output_dir}/{pickle_name}", 'wb') as p:
            pickle.dump(self.list_view_track_grain, p)

    def dump_parameters_as_json_file(self, json_name="parameters.json"):
        output_json = self.__dict__
        output_json.pop("list_view_track_grain")
        output_json.pop("list_xyz")
        output_json.pop("list_generated_range")
        with open(f"{self.output_dir}/{json_name}", 'w') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4) 


# this function returns n_random of (x,y,z) unit isotropic vector
def create_uniform_sphere_xyz():
    while True:
        xyz = np.random.normal(
            loc   = 0,
            scale = 1,
            size  = 3)
        if abs(xyz[2]) < 0.001:
            continue
        norm = np.linalg.norm(xyz, ord=2)
        if abs(norm) < 0.001:
            continue
        x,y,z = xyz / norm
        return [x,y,z]


if __name__ == "__main__":

    flag_debug = True
    if flag_debug:
        json_name = "maskrcnn_create_3d_simulated_grains_parameters.json"
        n_tracks = [80, 80]
        id_dataset = 5
    else:
        args = sys.argv
        json_name = args[1]
        n_tracks = int(args[2])
        id_dataset = int(args[3])

    gg = GrainGenator()
    gg.n_tracks = n_tracks
    gg.id_dataset = id_dataset
    gg.load_parameters_from_json(json_name)

    gg.create_output_dir()

    gg.generate_tracks_and_noises()

    gg.dump_pickle_file("grains.pickle")
    gg.dump_parameters_as_json_file("parameters.json")

