# file to store some often use functions
import os, sys, shutil
import os.path as osp
import multiprocessing as mp
import numpy as np
import cv2


def renew_dir(target_dir):
    if osp.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)


def build_dir(target_dir):
    if not osp.exists(target_dir):
        os.makedirs(target_dir)


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
