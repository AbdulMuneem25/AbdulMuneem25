import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import os
import pickle


if __name__ == '__main__':

    n_track = 1000
    crystal_distance = 0.06
    n_enough_crystal = int(n_track / crystal_distance)

    #fig = plt.figure()
    #plt.yscale('log')
    #ax = fig.add_subplot(111)
    thickness_boron = 0.200
    thickness_protection = 0.060
    depth_boron = thickness_boron + thickness_protection

    for prob_crystal_dev in np.arange(0.2, 0.06, -0.05):
        list_firstgrain = []
        for it in range(n_track):
            for ic in range(n_enough_crystal):
                reaction_point= np.random.uniform(depth_boron, thickness_protection)
                rand_number = random.uniform(0, 1)
                if rand_number < prob_crystal_dev:
                    difference =   ic - reaction_point 
                    list_firstgrain.append(difference)
                    break
        	
        
        bin_heights, bin_borders = np.histogram(list_firstgrain, 50, (0, 50))
        bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
        plt.errorbar(bin_middles, bin_heights, np.sqrt(bin_heights), (50 - 0) / (50 * 2), fmt='.', label=f'Prob: {prob_crystal_dev:.2f}')
        bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2


    plt.title('difference reaction point and fist grain')
    plt.xlabel('difference First developed grain and reaction point')
    plt.ylabel('counts')
    plt.legend()
    plt.savefig("reaction_point_-first_grain.png")

