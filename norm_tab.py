# This code is used to change the tab space from 2 to 4

import os, sys, shutil

def get_space_num(line):
    space_num = 0
    for c in line:
        if c!=' ':
            break
        else:
            space_num+=1
    return space_num

def check_tab_size(file_path):
    min_space_num = float('inf')
    with open(file_path, 'r') as in_f:
        for line in in_f:
            space_num = get_space_num(line)
            if space_num>0:
                min_space_num = min(space_num, min_space_num)
    return min_space_num

def get_file_list(norm_dir):
    file_list = list()
    for subdir, dirs, files in os.walk(norm_dir):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(subdir, file)
                tab_size = check_tab_size(full_path)
                if tab_size == 2:
                    file_list.append(full_path)
    return file_list

def norm_tab(file_list):
    for file_path in file_list:
        tmp_file_path = file_path.replace('.py','_tmp.py')
        shutil.copy2(file_path, tmp_file_path)
        with open(tmp_file_path,'r') as in_f,open(file_path,'w') as out_f:
            for line in in_f:
                space_num = get_space_num(line)
                out_f.write(' '*space_num*2 + line.lstrip())
        os.remove(tmp_file_path)


def main():
    norm_dir = './unit_4SpaceTab'
    file_list = get_file_list(norm_dir)
    norm_tab(file_list)


if __name__ == '__main__':
    main()