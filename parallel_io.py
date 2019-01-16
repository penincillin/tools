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


def save_pkl_parallel_list(res_dir, all_data):
    assert(type(all_data) == list)
    process_num = min(len(all_data), 32)
    pivot = len(all_data)//process_num
    process_list = list()
    for i in range(0, process_num+1):
        start = i*pivot
        end = min((i+1)*pivot, len(all_data))
        if start>=end: continue
        res_file = osp.join(res_dir, '{}.pkl'.format(i))
        p = mp.Process(target=save_pkl_single, \
                args=(res_file, all_data[start:end]))
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()


def save_pkl_parallel_dict(res_dir, all_data):
    assert(type(all_data) == dict)
    dict_keys = list(all_data.keys())
    process_num = min(len(dict_keys), 32)
    pivot = len(dict_keys)//process_num
    process_list = list()
    for i in range(0, process_num+1):
        start = i*pivot
        end = min((i+1)*pivot, len(all_data))
        if start>=end: continue
        res_file = osp.join(res_dir, '{}.pkl'.format(i))
        sub_data = { key: all_data[key] \
                    for key in dict_keys[start:end] }
        p = mp.Process(target=save_pkl_single, \
                args=(res_file, sub_data))
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()


def save_pkl_parallel(res_dir, all_data):
    if not osp.exists(res_dir):
        os.makedirs(res_dir)
    if type(all_data) == list:
        save_pkl_parallel_list(res_dir, all_data)
    elif type(all_data) == dict:
        save_pkl_parallel_dict(res_dir, all_data)
    else:
        print("Not supported class")





# load data from pkl
def get_pkl_file(pkl_dir):
    pkl_file_list = list()
    for subdir, dirs, files in os.walk(pkl_dir):
        for file in files:
            if file.find(".pkl")>=0:
                pkl_file_list.append(osp.join(subdir, file))
    return pkl_file_list


def load_pkl_single(pkl_file, py2to3):
    res_list = list()
    with open(pkl_file, 'rb') as in_f:
        if py2to3:
            single_data = pickle.load(in_f, encoding='latin1')
        else:
            single_data = pickle.load(in_f)
    return single_data


def load_pkl_parallel(pkl_dir, py2to3=False):

    pkl_file_list = get_pkl_file(pkl_dir)

    process_num = min(len(pkl_file_list), 32)
    pool = mp.Pool(process_num)
    args = [(pkl_file, py2to3) for pkl_file in pkl_file_list]
    result_list = pool.starmap(load_pkl_single, args)

    all_data = None
    if type(result_list[0])==list:
        all_data = list()
        for single_list in result_list:
            all_data += single_list
    elif type(result_list[0])==dict:
        all_data = dict()
        for single_dict in result_list:
            all_data.update(single_dict)
    else:
        print('Invalid Data Type')
    return all_data
