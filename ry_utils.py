# file to store some often use functions
import os, sys, shutil
import os.path as osp
import multiprocessing as mp
import numpy as np
import cv2
import pickle
import json


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
    build_dir(subdir_path)


def update_extension(file_path, new_extension):
    assert new_extension[0] == '.'
    old_extension = '.' + file_path.split('.')[-1]
    new_file_path = file_path.replace(old_extension, new_extension)
    return new_file_path


def get_all_files(in_dir, extension, path_type='full'):
    assert path_type in ['full', 'relative', 'name_only']
    assert isinstance(extension, str) or isinstance(extension, tuple)

    all_files = list()
    for subdir, dirs, files in os.walk(in_dir):
        for file in files:
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
    res_file_dir = '/'.join(res_file.split('/')[:-1])
    if len(res_file_dir)>0:
        if not osp.exists(res_file_dir):
            os.makedirs(res_file_dir)
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
