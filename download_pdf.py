import os, sys, shutil
import os.path as osp
import re
import requests

if __name__ == '__main__':


    pdf_pattern = re.compile(r'http:.*?\.pdf')
    name_pattern = re.compile(r'<td>[0-9a-zA-Z\s-]+</td>')

    pdf_dir = 'cmu_computer_vision'
    if osp.exists(pdf_dir):
        shutil.rmtree(pdf_dir)
    os.mkdir(pdf_dir)

    html_file = 'page.html'
    lecture_id = 0
    with open(html_file, 'r') as in_f:
        for line in in_f:
            urls = pdf_pattern.findall(line)
            if len(urls)>0:
                file_name = name_pattern.findall(line)[0]
                file_name = file_name.replace('<td>','').replace('</td>','')
                for i, url in enumerate(urls):
                    lec_prefix = '{}_{}'.format(lecture_id, \
                            '{}_'.format(i) if len(urls)>1 else '')
                    pdf_name = '{}{}.pdf'.format(lec_prefix, '_'.join(file_name.split()))
                    pdf_file_path = osp.join(pdf_dir, pdf_name)
                    with open(pdf_file_path, 'wb') as out_f:
                        response = requests.get(url)
                        out_f.write(response.content)
                    print('we have complete', pdf_name)
                lecture_id += 1
