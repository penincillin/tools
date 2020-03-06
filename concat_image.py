import os
import os.path as osp
import sys
import ry_utils
import numpy as np
import cv2


def get_all_names(all_dirs):
    all_names = list()
    for in_dir in all_dirs:
        img_names = list()
        for subdir, dirs, files in os.walk(in_dir):
            for file in files:
                if file.endswith(".png"):
                    img_names.append(osp.join(subdir, file).replace(in_dir, '')[1:])
        all_names += img_names
    all_names = sorted(list(set(all_names)))
    return all_names


def main():

    all_dirs = [
        'joints_21_ho3d_all',
        'mtc_hand_10_epoch',
        'mtc_hand_170_epoch',
        'mixture_mtc_hand/1e-3',
        'mixture_mtc_hand/1e-4'
    ]

    all_names = get_all_names(all_dirs)

    res_dir = "coco_concat"
    ry_utils.renew_dir(res_dir)
    for name in all_names:
        valid = True
        img_list = list()
        for in_dir in all_dirs:
            img_path = osp.join(in_dir, name)
            if osp.exists(img_path):
                img = cv2.imread(img_path)
                img_list.append(img)
            else:
                valid = False
                break
        if valid:
            res_subdir = osp.join(res_dir, '/'.join(name.split('/')[:-1]))
            ry_utils.build_dir(res_subdir)
            res_img = np.concatenate(img_list, axis=0)
            cv2.imwrite(osp.join(res_dir, name), res_img)


if __name__ == '__main__':
    main()
