import numpy as np
import cv2
import os
import math
import random
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import glob
import pickle
import sys
import json


if __name__ == "__main__":


    list_pickle = glob.glob('*.pickle')

    for p in list_pickle:
        #
        prob = float(p[0:3])*0.01
        with open(p, 'rb') as f:
            list_grain = pickle.load(f)
        #

        fig = plt.figure(dpi=100, figsize=(12,10))
        diff_root_firstgrain_x = []
        diff_root_firstgrain_y = []
        diff_bound_firstgrain_x = [] 
        diff_bound_firstgrain_y = [] 

        diff_root_firstgrain_x_center = []
        diff_bound_firstgrain_x_center = [] 

        for region in list_grain:
            for track in region:
                # track?
                if track["type"] != 't':
                    raise Exception("not track!!!")
                # grain
                first_grain = track["list_grain"][0]
                last_grain = track["list_grain"][-1]
                root = track["root"]
                # theta cut
                dx = last_grain[0] - first_grain[0]
                dy = last_grain[1] - first_grain[1]
                dz = last_grain[2] - first_grain[2]
                horizontal = math.sqrt(dx**2 + dy**2)
                tan_theta =   horizontal / dz
                this_theta = math.atan(tan_theta)
                if abs(this_theta) > 0.8:
                    continue
                #
                bound_x = -1.0 * (dx / dz) * root[2] + root[0]
                bound_y = -1.0 * (dy / dz) * root[2] + root[1]

                diff_root_firstgrain_x.append(first_grain[0] - root[0])
                diff_root_firstgrain_y.append(first_grain[1] - root[1])
                diff_bound_firstgrain_x.append(first_grain[0] - bound_x)
                diff_bound_firstgrain_y.append(first_grain[1] - bound_y)
                if abs(first_grain[1] - root[1]) < 0.1:
                    diff_root_firstgrain_x_center.append(first_grain[0] - root[0])
                if abs(first_grain[1] - bound_y) < 0.1:
                    diff_bound_firstgrain_x_center.append(first_grain[0] - bound_x)

        #
        ax = fig.add_subplot(2,2,1)
        H = ax.hist2d(diff_root_firstgrain_x, diff_root_firstgrain_y, bins=[np.linspace(-1.5, 1.5, 120),np.linspace(-1.5, 1.5, 120)], cmap=cm.jet)
        this_std = np.std(diff_root_firstgrain_x_center)
        ax.text(-0.1, 1.0, f'$\sigma$={this_std:.2f}', size=30, color="white")
        ax.set_title(f'difference: root - 1st_grain, prob={prob}')
        ax.set_xlabel('dx')
        ax.set_ylabel('dy')
        fig.colorbar(H[3],ax=ax)
        #
        ax = fig.add_subplot(2,2,2)
        H = ax.hist2d( diff_bound_firstgrain_x,  diff_bound_firstgrain_y, bins=[np.linspace(-1.5, 1.5, 120),np.linspace(-1.5, 1.5, 120)], cmap=cm.jet)
        this_std = np.std(diff_bound_firstgrain_x_center)
        ax.text(-0.1, 1.0, f'$\sigma$={this_std:.2f}', size=30, color="white")
        ax.set_title(f'difference: boundary - 1st_grain, prob={prob}')
        ax.set_xlabel('dx')
        ax.set_ylabel('dy')
        fig.colorbar(H[3],ax=ax)
        #

        ax = fig.add_subplot(2,2,3)
        H = ax.hist(diff_root_firstgrain_x_center, bins=np.linspace(-1.5, 1.5, 120))
        ax.set_title(f'difference: root - 1st_grain, prob={prob}')
        ax.set_xlabel('root point - 1st_grain')
        #ax.set_ylabel('dy')
        #

        ax = fig.add_subplot(2,2,4)
        H = ax.hist(diff_bound_firstgrain_x_center, bins=np.linspace(-1.5, 1.5, 120))
        ax.set_title(f'difference: boundary - 1st_grain, prob={prob}')
        ax.set_xlabel('boundary - 1st_grain')
        #ax.set_ylabel('dy')
        #
        fig.tight_layout()
        plt.savefig(f"displacement_prob_{prob:.2f}.png")






