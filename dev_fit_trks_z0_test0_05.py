import math
import glob
import itertools
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import minimize
import os
import matplotlib.cm as cm


def read_formatted_txt(filename, int_list=[]):
    mylist = []
    headers_name = []
    headers_type = []
    with open(filename, "r") as rf:
        for num, line in enumerate(rf):
            data = line.split()
            if num == 0:
                #print(data)
                for i in data:
                    i = i.replace('#', '')# remove sharp at the head in the header line
                    headers_name.append(i)
                    if i in int_list:
                        headers_type.append(int)
                    else:
                        headers_type.append(float)
            else:
                if line[0] == "#":
                    continue
                #print("{} {}".format(len(headers_type), len(data)))
                if len(headers_type) != len(data):
                    raise Exception("column number is inconsistent")
                items = {}
                for i in range(len(headers_name)):
                    items[headers_name[i]] = (headers_type[i])(data[i])
                #items["org_line"] = line
                mylist.append(items)                
        print('headers_name',headers_name)
        print('headers_type',headers_type)
        return mylist


def rename_line_params(line_params):
    for p in line_params:
        #print('p',p)
        yield p


def model_line(zs, line_params):
    model_xs = []
    model_ys = []
    tmp_ax, tmp_ay, x0, y0, z0 = rename_line_params(line_params)
    print('tmp_ax:',tmp_ax, 'tmp_ay:',tmp_ay, 'x0:',x0,'y0:',y0,'z0:',z0)
    for z in zs:
        ax = tmp_ax if z > z0 else - tmp_ax
        ay = tmp_ay if z > z0 else - tmp_ay
        x = x0 + ax * (z - z0)
        y = y0 + ay * (z - z0)
        model_xs.append(x)
        model_ys.append(y)
    return model_xs, model_ys


def calc_impact_factor_sq( x, y, z, line_params):
    tmp_ax, tmp_ay, x0, y0, z0 = rename_line_params(line_params)
    err_x = 0.04
    err_y = 0.04
    err_z = 0.06
    # real or mirror image
    ax = tmp_ax if z > z0 else -tmp_ax
    ay = tmp_ay if z > z0 else -tmp_ay
    # distance between a point and a line
    bx = x0 - ax * z0
    by = y0 - ay * z0
    a = (ax*(x-bx) + ay*(y-by) + 1.*(z)) / (ax*ax + ay*ay + 1.)
    xx = bx + ax * a
    yy = by + ay * a
    zz = 0. + 1. * a
    ip_sq  = (xx-x)**2 / err_x**2
    ip_sq += (yy-y)**2 / err_y**2
    ip_sq += (zz-z)**2 / err_z**2
    return ip_sq 


def sum_impact_factor_sq(line_params, points):
    sum_ip_sq = 0.0
    for p in points:
        sum_ip_sq += calc_impact_factor_sq(p['x'], p['y'], p['z'], line_params)
    return sum_ip_sq

if __name__ == "__main__":

    root_dir = "range_calc_kur_ill_data1/ill_not_goood_fitting"
    files = glob.glob(f'{root_dir}/*.txt')

    dist_rootpoint_fitpoint = []
    theta = []

    for f in files:
        basename = os.path.basename(f)

        points = read_formatted_txt(f)
        print('points',points)
        xs = [p['x'] for p in points]
        ys = [p['y'] for p in points]
        zs = [p['z'] for p in points]

        z_mid = (max(zs) + min(zs)) / 2.0
        y_mid = max(ys)
        x_mid = max(xs)

        xpoi =  xs[0]
        ypoi =  ys[0]
        zpoi =  zs[0]
        
        # fitting

        dx = x_mid - points[0]['x']
        dy = y_mid - points[0]['y'] 
        dz = max(zs) - points[0]['z']
        dxdz = dx/dz
        dydz = dy/dz
        print('dxdz', dxdz, 'dydz', dydz)
        #if dxdz and dydz < 0:
            #dxdz and dydz == 1 
        line_params_0 = [dxdz, dydz, points[0]['x'], points[0]['y'], points[0]['z']]
        #line_params_0 = [1.0, 1.0, points[0]['x'], points[0]['y'], points[0]['z']]

        #line_params_0 = [12.96067481,   2.66975119, -40.24160203, 390.90370922,20.34746237]
        #print('line_params_0',line_params_0)
        result = minimize(sum_impact_factor_sq, line_params_0, args=(points), tol=0.001)   ###tol=1e-2
        print('result:',result)
        line_params = result.x
        print('line_params:',line_params)
        dxdzfit, dydzfit, x0, y0, z0 = rename_line_params(line_params)
        print('----')       
        # 3d plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title("fitting result")
        ax.scatter3D(xs, ys, zs, marker='+', color="green")
        # line
        model_zs = np.linspace( max(zs), min(zs), 100)
        model_xs, model_ys = model_line(model_zs, line_params)
        #ax.plot(model_xs, model_ys, model_zs, "-", color="#00aa00")
        ax.plot(model_xs, model_ys, model_zs, "-", color="red")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        #print('model_xs',len(model_xs), 'model_ys', len(model_ys))
        
        print('basename',basename)
        plt.show()

        dist = np.sum(((x0-xpoi)**2+(y0-ypoi)**2+(z0-zpoi)**2), axis =0)
        dist_root_fitpoint = np.sqrt(dist)
        dist_rootpoint_fitpoint.append(dist_root_fitpoint)
        theta.append(dxdzfit)
    dist_rootpoint_fitpoint_micron = [aa*0.055 for aa in dist_rootpoint_fitpoint]
    #print('dist_rootpoint_fitpoint',dist_rootpoint_fitpoint_micron)
    #print('theta',theta)
        
    plt.clf()
    vals, bin_edges = np.histogram(dist_rootpoint_fitpoint_micron, 20,(0,4))
    #print(vals)
    this_std = np.std(dist_rootpoint_fitpoint_micron)
    bin_middles = 0.5*(bin_edges[1:] + bin_edges[:-1])
    plt.errorbar(bin_middles, vals, np.sqrt(vals),  4.0/20.0,fmt='o',color='g')
    plt.text( 2.0,max(vals)/1.3, f'$\sigma$={this_std:.2f}', size=30, color="black")
    plt.title('Distance fitting and first grain', fontsize = '22')
    plt.xlabel('range [$\mu$m]', fontsize = '16')
    plt.ylabel('Counts', fontsize = '16')
    plt.savefig(f"{root_dir}/distance.png")
    plt.clf()
    H = plt.hist2d(theta, dist_rootpoint_fitpoint_micron,  bins=[np.linspace(0,8,10), np.linspace(0, math.pi/2.0, 10)],cmap=cm.jet)
    plt.ylim(0, math.pi/2.0)
    plt.colorbar(H[3])
    plt.title("Distance-theta")
    plt.ylabel('distance [$\mu m$]')
    plt.xlabel('theta [rad]')
    plt.tight_layout()
    plt.savefig(f"{root_dir}/dist_theta_2Dhist.png")
    plt.clf()
    plt.scatter(theta, dist_rootpoint_fitpoint_micron)
    plt.ylabel('distance [$\mu m$]')
    plt.xlabel('theta [rad]')
    plt.tight_layout()
    plt.savefig(f"{root_dir}/dist_theta_scatter.png")


