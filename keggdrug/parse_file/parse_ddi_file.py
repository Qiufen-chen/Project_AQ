#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/21 23:12
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : parse_ddi_file.py
# @Software: PyCharm
'''

import os
import json
from pprint import pprint


def parse_ddi_file(file_path):

    index_dir = file_path + '/dataset/ddi_data/'
    save_dir = file_path + '/dataset/drug_json/'

    for (root, dirs, files) in os.walk(index_dir):
        for filename in files:
            ddi = {}
            ddi["DRUG_ID"] = str(filename).split('.')[0]
            with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                lines = f.readlines()

                partner_list = []
                for line in lines:
                    partner_dict = {}

                    partner_dict["DRUG_ID"] = str(line.split()[1]).split(':')[1].strip()

                    partner_dict['STATISTICAL_PARAMETER'] = line.split()[2].strip()

                    partner_dict['MEDICINE_ENZYME'] = {}
                    if line.find('P') == -1:
                        new_line = line[22:].strip()
                        if '/' in new_line and ':' in new_line:
                            element_list = new_line.replace('\t', '').replace('\n', '').split('/')
                            for i in range(len(element_list)):
                                partner_dict['MEDICINE_ENZYME'][element_list[i].split(':')[0].strip()] = \
                                    element_list[i].split(':')[1].strip()
                            partner_list.append(partner_dict)

                        elif ':' in new_line:
                            element_list = new_line.replace('\t', '').replace('\n', '').split('/')
                            for i in range(len(element_list)):
                                partner_dict['MEDICINE_ENZYME'][element_list[i].split(':')[0].strip()] = \
                                element_list[i].split(':')[1].strip()
                            partner_list.append(partner_dict)

                        else:
                            partner_dict['MEDICINE_ENZYME'] = new_line.strip()
                            partner_list.append(partner_dict)

                    else:
                        new_line = line[line.find('P')+1: ].strip()
                        if '/' in new_line and ':' in new_line:
                            element_list = new_line.replace('\t', '').replace('\n', '').split('/')
                            for i in range(len(element_list)):
                                partner_dict['MEDICINE_ENZYME'][element_list[i].split(':')[0].strip()] = \
                                    element_list[i].split(':')[1].strip()
                            partner_list.append(partner_dict)

                        elif ':' in new_line:
                            element_list = new_line.replace('\t', '').replace('\n', '').split('/')
                            for i in range(len(element_list)):
                                partner_dict['MEDICINE_ENZYME'][element_list[i].split(':')[0].strip()] = \
                                    element_list[i].split(':')[1].strip()
                            partner_list.append(partner_dict)

                        else:
                            partner_dict['MEDICINE_ENZYME'] = new_line.strip()
                            partner_list.append(partner_dict)

            ddi['PARTNER'] = partner_list
            json.dump(ddi, open(save_dir + str(filename).split('.')[0] + '.json', 'w'), ensure_ascii=False, indent=4)


def main():
    path = os.path.abspath(__file__).replace('\\', '/').rsplit('/', 2)[0]
    print(path)

    parse_ddi_file(path)


################################################################################################################
if __name__ == '__main__':
    main()
