import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import os
import pickle


if __name__ == '__main__':

    n_track = 100000
    n_enough_crystal = 1000

    fig = plt.figure()
    plt.yscale('log')
    ax = fig.add_subplot(111)


    for prob_crystal_dev in np.arange(0.3, 0.05, -0.05):
        list_firstgrain = []
        for it in range(n_track):
            for ic in range(n_enough_crystal):
                rand_number = random.uniform(0, 1)
                if rand_number < prob_crystal_dev:
                    list_firstgrain.append(ic)
                    break
        	
        
        bin_heights, bin_borders = np.histogram(list_firstgrain, 50, (0, 50))
        bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
        plt.errorbar(bin_middles, bin_heights/n_track, np.sqrt(bin_heights)/n_track, (50 - 0) / (50 * 2), fmt='.', label=f'Prob: {prob_crystal_dev:.2f}')
        bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2


    ax.set_title('Prob-first_grain')
    ax.set_xlabel('First developed grain')
    ax.set_ylabel('')
    ax.legend()
    plt.savefig("prob-first_grain.png")



"""

        fig = plt.figure(dpi=100, figsize=(10,10))





            ax = fig.add_subplot(2, 2, 1+i)
            n_bin = 20
            x_min = 0.0
            x_max = 10
            #p0 = [1.5, 0.0, 1.0, 4.0, 0.0, 1.0]

            bin_heights, bin_borders = np.histogram(list_range, n_bin, (x_min, x_max))
            bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
            plt.errorbar(bin_middles, bin_heights, np.sqrt(bin_heights), (x_max - x_min) / (n_bin * 2), fmt='o',color='g',label=f'N_track: {len(list_range)}')
            bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
            #popt, _ = curve_fit(bimodal, bin_centers, bin_heights, p0=p0)
            #print(f"parameters for curve_fit: {popt}")
            #x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)
            #text_legend_label = f"Li: {popt[0]:.3f} +- {popt[2]:.3f}\nHe: {popt[3]:.3f} +- {popt[5]:.3f}"

            #ax.plot(x_interval_for_fit, bimodal(x_interval_for_fit, *popt), color='red',lw=3, label=text_legend_label)   
            ax.set_title(f'{t}-Range')
"""

