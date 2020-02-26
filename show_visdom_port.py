import os
import os.path as osp
import sys
import shutil
import time
from datetime import datetime
import subprocess as sp

def check_port_valid(port_num):
    cmd = f"lsof -i:{port_num} > .usage.txt"
    os.system(cmd)
    with open(".usage.txt", "r") as in_f:
        lines = in_f.readlines()
        if len(lines) == 0:
            return False
        for line in lines:
            if line.find("learnfair")>=0:
                return False
        return True

def get_visdom_port():
    port_range = range(8098, 8120, 1)
    #port_range = range(8104, 8105, 1)
    for port_num in port_range:
       valid = check_port_valid(port_num)
       print(port_num, valid)

def main():
    get_visdom_port()

if __name__ == '__main__':
    main()
