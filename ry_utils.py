# file to store some often use functions
import os, sys, shutil
import os.path as osp
import multiprocessing as mp
import numpy as np
import cv2
import pickle


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
    with open(pkl_file, 'rb') as in_f:
        try:
            data = pickle.load(in_f)
        except UnicodeDecodeError:
            in_f.seek(0)
            data = pickle.load(in_f, encoding='latin1')
    return data


def draw_keypoints_each(image, keypoints, res_dir):
    if isinstance(image, str):
        image = cv2.imread(image)
    elif isinstance(image, np.ndarray):
        image = image
    else:
        print("Undefined image type")
        sys.exit(0)
    renew_dir(res_dir)
    for i in range(len(keypoints)):
        if len(keypoints[i]) > 2:
            x, y, score = keypoints[i]
            if score > 0.0:
                draw_image = image.copy()
                cv2.circle(draw_image, (int(x), int(y)), radius=5,
                           color=(0, 0, 255), thickness=-1)
        else:
            draw_image = image.copy()
            x, y = keypoints[i]
            cv2.circle(draw_image, (int(x), int(y)), radius=5,
                       color=(0, 0, 255), thickness=-1)
        cv2.imwrite('{0}/{1:02d}.png'.format(res_dir, i), draw_image)


def draw_keypoints(image, keypoints, res_img_path):
    if isinstance(image, str):
        image = cv2.imread(image)
    elif isinstance(image, np.ndarray):
        image = image
    else:
        print("Undefined image type")
        sys.exit(0)
    draw_image = image
    for i in range(len(keypoints)):
        if len(keypoints[i]) > 2:
            x, y, score = keypoints[i]
            if score > 0.0:
                cv2.circle(draw_image, (int(x), int(y)), radius=5,
                           color=(0, 0, 255), thickness=-1)
        else:
            x, y = keypoints[i]
            cv2.circle(draw_image, (int(x), int(y)), radius=5,
                       color=(0, 0, 255), thickness=-1)
    cv2.imwrite(res_image_path, draw_image)
