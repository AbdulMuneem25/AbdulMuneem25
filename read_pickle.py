import pickle
import glob


def read_binaryfiles(dir_path):
    binary_files = []
    image_path = f"{dir_path}"
    pic_file_names = glob.glob(f"{image_path}/grains.pickle")
    for pic in pic_file_names:
        with open(pic, "rb") as f:
            pic_files = pickle.load(f)
            binary_files.append(pic_files)
    return binary_files


if __name__ == "__main__":

    INPUT_DIR = "range_calc_kur_ill_data1"
    pick_file = read_binaryfiles(INPUT_DIR)
    print('--------')
