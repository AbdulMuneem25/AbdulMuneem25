import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
import sys
import glob
import pickle



if __name__ == '__main__':
   
    # read
    with open('list_condition.pickle', 'rb') as f:
        list_condition = pickle.load(f)
    print('---------')
    # loop
    list_result = [[],[]] # list_result[0] is for ILL, list_result[1] is for KUR 

    for i in range(2, len(list_condition)):
        for k in range(2):# ILL and KUR
            chisq = {"range_bin_heights": 0.0, "grains_bin_heights":0.0}
            for t in ["range_bin_heights", "grains_bin_heights"]:
                histogram_real = list_condition[k][t]
                histogram_sim = list_condition[i][t]
                histogram_sim = [x * sum(histogram_real) / sum(histogram_sim) for x in histogram_sim]
                
                if len(histogram_real) != len(histogram_sim):
                    raise Exception("different type!!")
                for j in range(len(histogram_real)):
                    if histogram_real[j] < 0.001:
                        continue
                    chi = ( histogram_real[j] - histogram_sim[j] ) / math.sqrt(histogram_real[j])
                    chisq[t] += chi**2

            result = {
                "name": list_condition[i]['name'],
                "chisq": chisq['range_bin_heights'] + chisq['grains_bin_heights'],
                "chisq_range": chisq['range_bin_heights'],
                "chisq_grains": chisq['grains_bin_heights']
            }
            list_result[k].append(result)
            #print(f"{list_condition[i]['name']} {k} {chisq['range_bin_heights']} {chisq['grains_bin_heights']} {chisq['range_bin_heights'] + chisq['grains_bin_heights']} ")


    list_combination_search = []
    for ill in list_result[0]:
        for kur in list_result[1]:
            if ill["name"][:33] != kur["name"][:33]:
                continue
            com = {
                "ill_name": ill["name"],
                "kur_name": kur["name"],
                "ill_chisq": ill["chisq"],
                "kur_chisq": kur["chisq"],
                "ill_chisq_range": ill["chisq_range"],
                "kur_chisq_range": kur["chisq_range"],
                "ill_chisq_grains": ill["chisq_grains"],
                "kur_chisq_grains": kur["chisq_grains"],
                "total_chisq": ill["chisq"] + kur["chisq"],
                "total_chisq_range": ill["chisq_range"] + kur["chisq_range"],
                "total_chisq_grains": ill["chisq_grains"] + kur["chisq_grains"]
            }
            list_combination_search.append(com)

    list_combination_search_sorted = sorted(list_combination_search, key=lambda x:x['total_chisq'])
    for i in range(5):
        print(list_combination_search_sorted[i])

    print("====")
    list_combination_search_sorted = sorted(list_combination_search, key=lambda x:x['total_chisq_range'])
    for i in range(5):
        print(list_combination_search_sorted[i])

    print("====")
    list_combination_search_sorted = sorted(list_combination_search, key=lambda x:x['total_chisq_grains'])
    for i in range(5):
        print(list_combination_search_sorted[i])

