import os
import os.path as osp
import ry_utils
import numpy as np
import cv2

def main():
    '''
    root_dir = '1e-3_lr_decay_epoch_200'
    all_dirs = [
        #osp.join(root_dir, 'scale_position'),
        osp.join(root_dir, 'all_augment')
    ]

    all_dirs.append("color_jittering")
    #all_dirs.append("color_jittering_compare")
    all_dirs.append("joints_21_no_shape_params")
    '''

    all_dirs = [
        'joints_16_ho3d_wrong_split/color_jittering',
        'joints_21/top_finger_manual/1e-4_cj_augment_finetune',
        'joints_21/top_finger_manual/1e-3_cj_ho3d_all'
    ]
    

    all_names = list()
    for in_dir in all_dirs:
        img_names = os.listdir(in_dir)
        all_names += img_names
    all_names = list(set(all_names))

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
            res_img = np.concatenate(img_list, axis=0)
            cv2.imwrite(osp.join(res_dir, name), res_img)


if __name__ == '__main__':
    main()
