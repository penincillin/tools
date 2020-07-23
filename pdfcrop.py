import os, sys, shutil
import os.path as osp
import multiprocessing as mp

def crop_pdf(pdf_path):
    cmd = f"pdfcrop {pdf_path} {pdf_path}"
    os.system(cmd)

def main():
    p_list = list()
    for subdir, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = osp.join(subdir, file)
                p = mp.Process(target=crop_pdf, args=(pdf_path,))
                p.start()
                p_list.append(p)
    for p in p_list:
        p.join()

if __name__ == '__main__':
    main()
