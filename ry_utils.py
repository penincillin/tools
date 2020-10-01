# file to store some often use functions
import os, sys, shutil
import os.path as osp
import multiprocessing as mp
import numpy as np
import cv2
import pickle
import json
import subprocess as sp


def renew_dir(target_dir):
    if osp.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)


def build_dir(target_dir):
    if not osp.exists(target_dir):
        os.makedirs(target_dir)


def get_subdir(in_path):
    subdir_path = '/'.join(in_path.split('/')[:-1])
    return subdir_path

def make_subdir(in_path):
    subdir_path = get_subdir(in_path)
    if len(subdir_path) > 0:
        build_dir(subdir_path)


def update_extension(file_path, new_extension):
    assert new_extension[0] == '.'
    old_extension = '.' + file_path.split('.')[-1]
    new_file_path = file_path.replace(old_extension, new_extension)
    return new_file_path


def analyze_path(input_path):
    # assume input_path is the path of a file not a directory
    record = input_path.split('/')
    input_dir = '/'.join(record[:-1])
    file_name = record[-1]
    assert file_name.find(".")>0
    ext = file_name.split('.')[-1]
    file_basename = '.'.join(file_name.split('.')[:-1])
    return input_dir, file_name, file_basename, ext


def get_all_files(in_dir, extension, path_type='full', keywords=''):
    assert path_type in ['full', 'relative', 'name_only']
    assert isinstance(extension, str) or isinstance(extension, tuple)
    assert isinstance(keywords, str)
    assert osp.exists(in_dir)

    all_files = list()
    for subdir, dirs, files in os.walk(in_dir):
        for file in files:
            if len(keywords)>0:
                if file.find(keywords)<0: 
                    continue
            if file.endswith(extension):
                if path_type == 'full':
                    file_path = osp.join(subdir, file)
                elif path_type == 'relative':
                    file_path = osp.join(subdir, file).replace(in_dir, '')
                    if file_path.startswith('/'):
                        file_path = file_path[1:]
                else:
                    file_path = file
                all_files.append(file_path)
    return sorted(all_files)


def remove_swp(in_dir):
    remove_files = list()
    for subdir, dirs, files in os.walk(in_dir):
        for file in files:
            if file.endswith('.swp'):
                full_path = osp.join(subdir,file)
                os.remove(full_path)


def remove_pyc(in_dir):
    remove_files = list()
    for subdir, dirs, files in os.walk(in_dir):
        for file in files:
            if file.endswith('.pyc'):
                full_path = osp.join(subdir,file)
                os.remove(full_path)


def md5sum(file_path):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as in_f:
        hash_md5.update(in_f.read())
    return hash_md5.hexdigest()


# save data to pkl
def save_pkl(res_file, data_list, protocol=-1):
    assert res_file.endswith(".pkl")
    make_subdir(res_file)
    with open(res_file, 'wb') as out_f:
        if protocol==2:
            pickle.dump(data_list, out_f, protocol=2)
        else:
            pickle.dump(data_list, out_f)


def load_pkl(pkl_file, res_list=None):
    assert pkl_file.endswith(".pkl")
    with open(pkl_file, 'rb') as in_f:
        try:
            data = pickle.load(in_f)
        except UnicodeDecodeError:
            in_f.seek(0)
            data = pickle.load(in_f, encoding='latin1')
    return data


def load_json(in_file):
    assert in_file.endswith(".json")
    with open(in_file, 'r') as in_f:
        all_data = json.load(in_f)
        return all_data


def save_json(out_file, data):
    assert out_file.endswith(".json")
    with open(out_file, "w") as out_f:
        json.dump(data, out_f)


def load_npz(npz_file):
    res_data = dict()
    assert npz_file.endswith(".npz")
    raw_data = np.load(npz_file, mmap_mode='r')
    for key in raw_data.files:
        res_data[key] = raw_data[key]
    return res_data


def update_npz_file(npz_file, new_key, new_data):
    # load original data
    assert npz_file.endswith(".npz")
    raw_data = np.load(npz_file, mmap_mode='r')
    all_data = dict()
    for key in raw_data.files:
        all_data[key] = raw_data[key]
    # add new data && save
    all_data[new_key] = new_data
    np.savez(npz_file, **all_data)


def save_mesh_to_obj(obj_path, verts, faces=None):
    assert isinstance(verts, np.ndarray)
    assert isinstance(faces, np.ndarray)

    with open(obj_path, 'w') as out_f:
        # write verts
        for v in verts:
            out_f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        # write faces 
        if faces is not None:
            faces = faces.copy() + 1
            for f in faces:
                out_f.write(f"f {f[0]} {f[1]} {f[2]}\n")


""" 
following code is used to update ry_utils.py to conda envs
"""

def  __get_site_pacakge_dir(in_dir):
    in_dir = osp.join(in_dir, "lib")
    for subdir in os.listdir(in_dir):
        if subdir.find("python3")>=0 and subdir.find("lib")<0:
            sp_path = osp.join(in_dir, subdir, "site-packages")
            assert osp.exists(sp_path)
            return sp_path


def __get_conda_info():
    cmd = "conda env list"
    conda_env_output = sp.check_output(cmd.split()).decode('utf-8')
    dir_list = list()
    for line in conda_env_output.split():
    #for line in conda_env_output.split('/n'):
        for item in line.split():
            item = item.strip()
            if item[0] == '/':
                assert osp.exists(item)
                sp_path = __get_site_pacakge_dir(item)
                dir_list.append(sp_path)
    return dir_list
                

def __update_ry_utils():
    assert osp.exists("ry_utils.py")
    sp_dir_list = __get_conda_info()

    for sp_dir in sp_dir_list:
        res_file = osp.join(sp_dir, "ry_utils.py")
        shutil.copy2("ry_utils.py", res_file)
        print(res_file)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "update":
            __update_ry_utils()
