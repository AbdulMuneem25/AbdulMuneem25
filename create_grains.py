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


sys.path.append('../')
import maskrcnn_create_3d_simulated_grains



if __name__ == "__main__":

    json_name = "maskrcnn_create_3d_simulated_grains_parameters.json"

    for i in range(5, 31, 5):
        gg = maskrcnn_create_3d_simulated_grains.GrainGenator()
        gg.load_parameters_from_json(json_name)
        gg.output_dir = "."
        gg.probability_development = [i*0.01, i*0.01]
        gg.generate_tracks_and_noises()
        gg.dump_pickle_file(f"{i:03d}.pickle")
        gg.dump_parameters_as_json_file(f"parameters_{i:03d}.json")

