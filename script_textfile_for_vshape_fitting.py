import pickle
import matplotlib.pyplot as plt
import numpy as np
import math
from   math import pow, sqrt
import matplotlib.pyplot as plt
import random
import sys



def read_track_chained_txt(filename, category=1):
 
    xyzs = []
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line:
                break
            if len(line) == 1:
                continue
            if line[0] == "#":
                continue
            item_list = line.split()
            this_category = int(item_list[0])
            x = float(item_list[1]) 
            y = float(item_list[2])
            z = float(item_list[3]) 
            if this_category == category:
                xyzs.append([x, y, z])

    return xyzs



def dump_intobinaryfile(picklefile, dir_path):
    with open(f"{dir_path}/grains.pickle", "wb") as f:
        pickle.dump(picklefile, f)
    return


if __name__ == '__main__':
    dataset = "range_calc_kur_ill_data1"
    dir_path = f"{dataset}"
    view_names = ["kur"]
    #view_names = ["ill_dataset"]
    for view_name in view_names:
        xyzs = read_track_chained_txt(f"{dir_path}/{view_name}/Real_mirror_Track7.txt")
    
    xyz_points_seg = []
    x = []
    y = []
    z = []
    for i, m in enumerate(xyzs):
        #if m[0] and m[1] and m[2]!=0:
        #xyz_points_seg.append([#xyz])

        x_point = m[0] 
        y_point = m[1] 
        z_point = m[2] 
        if x_point and y_point and z_point != 0:
            #continue
   
            xyz_points_seg.append([x_point, y_point, z_point])
            x.append(x_point)
            y.append(y_point)
            z.append(z_point)
    print('xyz_points_seg',xyz_points_seg)
    print('xyzs',xyzs)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("fitting result")
    ax.scatter3D(x, y, z, marker='+', color="green")
    plt.show()

    with open(f"{dataset}/grains7.txt", 'w') as file:
        file.write("#x y z \n")
        for m, n, i in zip(x, y, z):
            file.write("{0} {1} {2}\n".format(m,n,i))