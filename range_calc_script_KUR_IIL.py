import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import glob
import pickle

sys.path.append('../')
import file_io_01



def gaussian(x, mean, amplitude, standard_deviation):
    return amplitude * np.exp( - ((x - mean) / standard_deviation) ** 2)

def bimodal(x, mean1, amplitude1, standard_deviation1, mean2, amplitude2, standard_deviation2):
    g0 = gaussian(x, mean1, amplitude1, standard_deviation1)
    g1 = gaussian(x, mean2, amplitude2, standard_deviation2)
    return  g0 + g1



if __name__ == '__main__':
   
    #list_text = glob.glob('track_*_Track.txt')
    list_text = glob.glob('*_Track.txt')


    params = {  "pix_x": 0.0549, # 50micron / ~909pixels
            "pix_y": 0.0549, # 50micron / ~909pixels
            "z_pitch": 20.0 / 55.0, # 20micron / 55layers
            "shrinkage_factor": 1.0 / 0.6 # nominal value
        }

    for j in range(0, len(list_text), 2):
        print(f"{j} in {len(list_text)}")
        type1 = list_text[j+0][:-10]
        type2 = list_text[j+1][:-10]

        fig = plt.figure(dpi=100, figsize=(10,10))

        for i, t in enumerate([type1, type2]):

            input_file = f"{t}_Track.txt"
            list_tracks = file_io_01.read_track_chained_txt(input_file, params)
            list_range = []
            list_n_grain = []
            for x in list_tracks:
                if abs(x["theta"]) > 0.8:
                    continue
                list_range.append(x["range"])
                list_n_grain.append(len(x["points"]))


            ax = fig.add_subplot(2, 2, 1+i)
            n_bin = 20
            x_min = 0.0
            x_max = 10
            p0 = [1.5, 0.0, 1.0, 4.0, 0.0, 1.0]


            bin_heights, bin_borders = np.histogram(list_range, n_bin, (x_min, x_max))
            bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
            plt.errorbar(bin_middles, bin_heights, np.sqrt(bin_heights), (x_max - x_min) / (n_bin * 2), fmt='o',color='g',label=f'N_track: {len(list_range)}')
            bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
            popt, _ = curve_fit(bimodal, bin_centers, bin_heights, p0=p0)
            print(f"parameters for curve_fit: {popt}")
            x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)
            text_legend_label = f"Li: {popt[0]:.3f} +- {popt[2]:.3f}\nHe: {popt[3]:.3f} +- {popt[5]:.3f}"

            ax.plot(x_interval_for_fit, bimodal(x_interval_for_fit, *popt), color='red',lw=3, label=text_legend_label)   
            ax.set_title(f'{t}-Range')
            ax.set_xlabel('range [$\mu$m]')
            ax.legend()


            ax = fig.add_subplot(2, 2, 3+i)
            n_bin = 20
            x_min = 0.0
            x_max = 40

            bin_heights, bin_borders = np.histogram(list_n_grain, n_bin, (x_min, x_max))
            bin_middles = 0.5*(bin_borders[1:] + bin_borders[:-1])
            plt.errorbar(bin_middles, bin_heights, np.sqrt(bin_heights), (x_max - x_min) / (n_bin * 2), fmt='o',color='g',label=f'N_track: {len(list_range)}')
            bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
            
            ax.set_title(f'{t}-number of grain')
            ax.set_xlabel('number of grain')
            ax.legend()


        fig.tight_layout()
        plt.savefig(f"Range_grain_{type1}_{type2}.png")
