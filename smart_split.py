import numpy as np


def split1(num_total, num_split):

    num_each = num_total // num_split

    for i in range(num_split):
        start = i*num_each
        end = (i+1)*num_each if i<num_split-1 else num_total
        print(i, end-start)


def split2(num_total, num_split):

    num_each = num_total // num_split + 1

    for i in range(num_split):
        start = i * num_each
        end = min((i+1) * num_each, num_total)
        if start < end:
            print(i, end-start, start, end)


def main():
    num_total = 100
    num_split = 10
    split2(num_total, num_split)


if __name__ == '__main__':
    main()
