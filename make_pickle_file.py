import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import glob
import pickle

sys.path.append('../')
import file_io


if __name__ == '__main__':
   
    list_sim = glob.glob('track_*_Track.txt')
    list_real = ['ILL_Track.txt', 'KUR_Track.txt']

    params = {  "pix_x": 0.0549, # 50micron / ~909pixels
            "pix_y": 0.0549, # 50micron / ~909pixels
            "z_pitch": 20.0 / 55.0, # 20micron / 55layers
            "shrinkage_factor": 1.0 / 0.6 # nominal value
        }

    list_condition = []
    for sr in [list_real, list_sim]:
        for j in sr:
            # read
            input_file = j
            print(j)
            list_tracks = file_io.read_track_chained_txt(input_file, params)
            # making list
            list_range = []
            list_n_grain = []
            for x in list_tracks:
                if abs(x["theta"]) > 0.8:
                    continue
                list_range.append(x["range"])
                list_n_grain.append(len(x["points"]))
            # 
            n_bin = 20
            x_min = 0.0
            x_max = 10
            range_bin_heights, range_bin_borders = np.histogram(list_range, n_bin, (x_min, x_max))
            # 
            n_bin = 20
            x_min = 0.0
            x_max = 40
            grains_bin_heights, grains_bin_borders = np.histogram(list_n_grain, n_bin, (x_min, x_max))
            # 
            this_condition = {
                "name": input_file,
                "range_bin_heights": range_bin_heights,
                #"range_bin_borders": range_bin_borders,
                "grains_bin_heights": grains_bin_heights,
                #"grains_bin_borders": grains_bin_borders,
            }
            list_condition.append(this_condition)


    with open('list_condition.pickle', 'wb') as f:
        pickle.dump(list_condition, f)