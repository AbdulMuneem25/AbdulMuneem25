import numpy as np
import matplotlib.pyplot as plt
import random
import os
import pickle

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


def create_Track_txt(track_ranges_micron, sigma_track_range, crystal_distance, prob_crystal_dev):
    n_track = 50
    thickness_boron = 0.200
    thickness_protection = 0.060
    depth_boron = thickness_boron + thickness_protection
    reaction_point= np.random.uniform(depth_boron, thickness_protection)

    file_output = f"track_{track_ranges_micron}_sig_{sigma_track_range:.2f}_crystal_{crystal_distance:.2f}_prob_{prob_crystal_dev:.2f}_Track.txt"

    # loop
    list_tracks = []
    for _ in range(n_track):
        track_base = random.choice([track_ranges_micron, track_ranges_micron*5.1/2.6])
        track_range_base = track_base + reaction_point
        track_range = track_range_base + random.gauss(0, sigma_track_range)

        n_crystal = int(track_range / crystal_distance)
        list_grain_position = []
        for c in range(n_crystal):
            p = (c + 0.5) * crystal_distance
            rand_number = random.uniform(0, 1)
            if rand_number < prob_crystal_dev:
                
                list_grain_position.append(p)
            #print(f"track:{i}, crystal:{c}, random_number:{rand_number:.3f}, position{p:.3f}")

        this_track = {"track_range_base":track_range_base,
                      "track_range": track_range,
                      "list_grain_position": list_grain_position}
        list_tracks.append(this_track)
    #print(list_tracks)


    list_str_out = []
    for t in list_tracks:
        if len(t["list_grain_position"]) > 0:
            for g in t["list_grain_position"]:
                list_str_out.append( f"1  0.0  0.0  {g*0.6*(55.0/20.0):.3f}\n" )
            list_str_out.append( f"1  0.0  0.0  0.0\n" )
            list_str_out.append( f"1  0.0  0.0  0.0\n" )


    with open(file_output, mode='w') as f:
        f.writelines(list_str_out)





if __name__ == '__main__':

    # output dir
    output_dir = 'monte_carlo_simulation_range_emulsion'
    os.makedirs(f"{output_dir}", exist_ok=True)
    #np.random.seed(0)

    # parameters   
    track_range_micron = [2.4, 2.6, 2.8, 3.0, 3.2]
    sigma_track_range = [0.5, 0.6, 0.7, 0.8, 0.9]
    crystal_distance = [0.04, 0.06]
    prob_crystal_dev = [0.07, 0.15]
    

    for r in track_range_micron:
        for s in sigma_track_range:
            for d in crystal_distance:
                for p in prob_crystal_dev:
                    print(r, s, d, p)
                    create_Track_txt(r, s, d, p)
