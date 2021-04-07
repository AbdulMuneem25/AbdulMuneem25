import numpy as np
import math


def read_track_chained_txt(filename, params, category=1):
    """
    filename: textfile to read
    params: "pix_x", "pix_y", "z_pitch", "shrinkage_factor"
    return: list of tracks
    """
    pix_size_x = params["pix_x"]
    pix_size_y = params["pix_y"]
    z_pitch = params["z_pitch"]
    shrinkage_factor = params["shrinkage_factor"]
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
    tracks_tmp = []
    for i, p in enumerate(xyzs):
        if i == 0:
            t = []

        if math.sqrt(p[0]**2 + p[1]**2 + p[2]**2) <0.01:
            tracks_tmp.append(t)
            t = []
        else:
            t.append(p)
    #
    tracks_tmp2 = [x for x in tracks_tmp if len(x) > 0]
    #
    tracks = []
    for tt2 in tracks_tmp2:
        t = {
            "points": tt2,
            "x0": tt2[0][0],
            "y0": tt2[0][1],
            "z0": tt2[0][2],
            "x1": tt2[-1][0],
            "y1": tt2[-1][1],
            "z1": tt2[-1][2],
            "dx": (tt2[-1][0] - tt2[0][0]) * pix_size_x,
            "dy": (tt2[-1][1] - tt2[0][1]) * pix_size_y,
            "dz": (tt2[-1][2] - tt2[0][2]) * z_pitch * shrinkage_factor,
            "dz_obs": (tt2[-1][2] - tt2[0][2]) * z_pitch
        }
        t["range"] = math.sqrt(t["dx"]**2 + t["dy"]**2 + t["dz"]**2)
        t["phi"] = math.atan2(t["dy"], t["dx"])
        if abs(t["dz"]) < 0.0001:
            this_theta = math.pi / 2.0
        else:
            horizontal = math.sqrt(t["dx"]**2 + t["dy"]**2)
            tan_theta =   horizontal / t["dz"]
            this_theta = math.atan(tan_theta)
        t["theta"] = this_theta
        tracks.append(t)
    return tracks, tracks_tmp2


def read_track_paird_txt(filename, params, category=1):
    """
    filename: textfile to read
    params: "pix_x", "pix_y", "z_pitch", "shrinkage_factor"
    return: list of tracks
    """
    pix_size_x = params["pix_x"]
    pix_size_y = params["pix_y"]
    z_pitch = params["z_pitch"]
    shrinkage_factor = params["shrinkage_factor"]
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
    tracks = []
    xyzs_even = xyzs[::2]
    xyzs_odd = xyzs[1::2]
    for i in range(len(xyzs_even)):
        p0 = xyzs_even[i]
        p1 = xyzs_odd[i]
        t = {
            "x0": p0[0],
            "y0": p0[1],
            "z0": p0[2],
            "x1": p1[0],
            "y1": p1[1],
            "z1": p1[2],
            "dx": (p1[0] - p0[0]) * pix_size_x,
            "dy": (p1[1] - p0[1]) * pix_size_y,
            "dz": (p1[2] - p0[2]) * z_pitch * shrinkage_factor,
            "dz_obs": (p1[2] - p0[2]) * z_pitch
        }
        t["range"] = math.sqrt(t["dx"]**2 + t["dy"]**2 + t["dz"]**2)
        t["phi"] = math.atan2(t["dy"], t["dx"])
        if t["dz"] < 0.0001:
            this_theta = math.pi / 2.0
        else:
            horizontal = math.sqrt(t["dx"]**2 + t["dy"]**2)
            tan_theta =   horizontal / t["dz"]
            this_theta = math.atan(tan_theta)
        t["theta"] = this_theta
        tracks.append(t)
    return tracks


def read_grid_txt(filename, category=3):
    """
    filename: textfile to read
    params: "pix_x", "pix_y", "z_pitch", "shrinkage_factor"
    return: list of tracks
    """
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


def combine_segment_to_track(segments):
    start_seg_ids = [0]
    end_seg_ids = []
    for i, s in enumerate(segments):
        if s["range"] < 0.001:
            start_seg_ids.append(i+1)
            end_seg_ids.append(i-1)
    end_seg_ids.append(len(segments)-1)
    #
    tracks = []
    for i, s in enumerate(segments):
        if i in start_seg_ids:
            t = {"x0": s["x0"],
                 "y0": s["y0"],
                 "z0": s["z0"],
                 "theta": s["theta"],
                 "phi": s["phi"],
                 "range": 0.0,
                 "dx": 0.0,
                 "dy": 0.0,
                 "dz": 0.0,
                 "dz_obs": 0.0
                }
        #
        t["range"] += s["range"]
        t["dx"] += s["dx"]
        t["dy"] += s["dy"]
        t["dz"] += s["dz"]
        t["dz_obs"] += s["dz_obs"]
        #
        if i in end_seg_ids:
            t["x1"] = s["x1"]
            t["y1"] = s["y1"]
            t["z1"] = s["z1"]
            tracks.append(t)
    return tracks



def re_calcurate_angle_of_track(tracks, params):
    pix_size_x = params["pix_x"]
    pix_size_y = params["pix_y"]
    z_pitch = params["z_pitch"]
    shrinkage_factor = params["shrinkage_factor"]
    for i, t in enumerate(tracks):
        t['dx'] = (t['x1']  - t['x0']) * pix_size_x
        t['dy'] = (t['y1']  - t['y0']) * pix_size_y
        t['dz'] = (t['z1']  - t['z0']) * z_pitch * shrinkage_factor
        t["phi"] = math.atan2(t["dy"], t["dx"])
        if t["dz"] < 0.0001:
            this_theta = math.pi / 2.0
        else:
            horizontal = math.sqrt(t["dx"]**2 + t["dy"]**2)
            tan_theta =   horizontal / t["dz"]
            this_theta = math.atan(tan_theta)
        t["theta"] = this_theta
    return tracks




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
        return mylist
