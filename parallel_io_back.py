import os, sys, shutil
import os.path as osp
import multiprocessing as mp
import pickle
import time

# save data to pkl
def save_pkl_single(res_file, data_list):
    res_file_dir = '/'.join(res_file.split('/')[:-1])
    if len(res_file_dir)>0:
        if not osp.exists(res_file_dir):
            os.makedirs(res_file_dir)
    with open(res_file, 'wb') as out_f:
        pickle.dump(data_list, out_f)

def save_pkl_parallel(res_dir, data_list):
    if not osp.exists(res_dir):
        os.makedirs(res_dir)
    process_num = min(len(data_list), 32)
    #process_num = 1
    pivot = len(data_list)//process_num
    process_list = list()
    for i in range(0, process_num+1):
        start = i*pivot
        end = min((i+1)*pivot, len(data_list))
        if start>=end: continue
        res_file = osp.join(res_dir, '{}.pkl'.format(i))
        p = mp.Process(target=save_pkl_single, \
                args=(res_file, data_list[start:end]))
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()


# load data from pkl
def get_pkl_file(pkl_dir):
    pkl_file_list = list()
    for subdir, dirs, files in os.walk(pkl_dir):
        for file in files:
            if file.find(".pkl")>=0:
                pkl_file_list.append(osp.join(subdir, file))
    return pkl_file_list


def load_pkl_single(pkl_file, res_list=None):
    if res_list is None:
        res_list = list()
    with open(pkl_file, 'rb') as in_f:
        single_data_list = pickle.load(in_f, encoding='latin1')
        for data in single_data_list:
            res_list.append(data)
    return res_list


def load_pkl_parallel(pkl_dir):
    #print(pkl_dir)
    pkl_file_list = get_pkl_file(pkl_dir)
    process_num = min(len(pkl_file_list), 32)
    pool = mp.Pool(process_num)
    result_list = pool.map(load_pkl_single, pkl_file_list)
    data_list = []
    for single_list in result_list:
        data_list += single_list
    return data_list
