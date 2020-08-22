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



def parse_ddi_file(index_dir, save_dir):
    """
    purpose: parse keggdrug_ddi fife,such as:
    '''
    dr:D00136	dr:D00147	P	unclassified
    dr:D00136	dr:D00184	P	Enzyme: CYP3A4 / CYP inhibition: CYP3A4
    dr:D00136	dr:D00210	P	unclassified
    dr:D00136	dr:D00211	P	CYP induction: CYP3A4
    dr:D00136	dr:D00228	P	Enzyme: CYP2D6
    dr:D00136	dr:D00232	P	unclassified
    dr:D00136	dr:D00252	P	Enzyme: CYP3A4 / CYP induction: CYP3A4
    dr:D00136	dr:D00253	P	unclassified
    dr:D00136	dr:D00270	P	Enzyme: CYP2D6 / Target: DRD2 / CYP inhibition: CYP2D6
    dr:D00136	dr:D00276	P	Enzyme: CYP3A4 / CYP inhibition: CYP3A4
    '''
    :param index_dir:
    :return:
    """
    for (root, dirs, files) in os.walk(index_dir):
        for filename in files:

            ddi = {}

            drugID_1 = str(filename).split('.')[0]
            ddi['drug_id'] = drugID_1

            with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                lines = f.readlines()

                partner_list = []

                for line in lines:
                    partner_dict = {}
                    # Gets the contents of the second column
                    drugID_2 = str(line.split()[1])

                    if drugID_2[0:3] == 'cpd':
                        cpd_id = drugID_2.split(':')[1]
                        partner_dict['cpd_id'] = cpd_id
                        pprint(partner_dict)

                    else:
                        drug_id = drugID_2.split(':')[1]
                        partner_dict['drug_id'] = drug_id
                        pprint(partner_dict)

                    # Gets the contents of the third column
                    statistical_parameter = line.split()[2]
                    partner_dict['statistical_parameter'] = statistical_parameter

                    # Gets the contents of the forth column
                    last_element_dic = {}
                    if ('unclassified' not in line) and ('CI,P' in line):
                        last_value = line[24:]
                        if '/' in last_value:
                            element_list = last_value.replace('\t', '').replace('\n', '').strip().split('/')
                            # print(element_list)

                            # list to dictionary
                            for i in range(len(element_list)):
                                last_element_dic[element_list[i].split(':')[0].strip()] = element_list[i].split(':')[1].strip()
                            partner_dict['medicine_enzyme'] = last_element_dic
                            partner_list.append(partner_dict)

                        else:
                            element_list = []
                            element = last_value.replace('\n','').replace('\t','')
                            # pprint(element)
                            element_list.append(element)

                            for i in range(len(element_list)):
                                last_element_dic[element_list[i].split(':')[0].strip()] = element_list[i].split(':')[1].strip()
                            partner_dict['medicine_enzyme'] = last_element_dic
                            partner_list.append(partner_dict)


                    elif ('unclassified' not in line) and ('CI' in line) and ('same components' not in line):
                        last_value = line[22:]
                        if '/' in last_value:
                            element_list = last_value.replace('\t', '').replace('\n', '').strip().split('/')
                            # pprint(element_list)

                            # List to dictionary
                            for i in range(len(element_list)):
                                last_element_dic[element_list[i].split(':')[0].strip()] = element_list[i].split(':')[1].strip()
                            partner_dict['medicine_enzyme'] = last_element_dic
                            partner_list.append(partner_dict)

                        else:
                            element_list = []
                            element = last_value.replace('\n', '').replace('\t', '')
                            # pprint(element)
                            element_list.append(element)

                            for i in range(len(element_list)):
                                last_element_dic[element_list[i].split(':')[0].strip()] = element_list[i].split(':')[1].strip()

                            partner_dict['medicine_enzyme'] = last_element_dic
                            partner_list.append(partner_dict)

                    elif ('unclassified' not in line) and ('P' in line) and ('same components' not in line):
                        last_value = line[21:]
                        if '/' in last_value:
                            element_list = last_value.replace('\t', '').replace('\n', '').split('/')
                            # pprint(element_list)

                            for i in range(len(element_list)):
                                last_element_dic[element_list[i].split(':')[0].strip()] = element_list[i].split(':')[1].strip()
                            partner_dict['medicine_enzyme'] = last_element_dic
                            partner_list.append(partner_dict)

                        else:
                            element_list = []
                            element = last_value.replace('\n', '').replace('\t', '')
                            # pprint(element)
                            element_list.append(element)

                            for i in range(len(element_list)):
                                last_element_dic[element_list[i].split(':')[0].strip()] = element_list[i].split(':')[1].strip()
                            partner_dict['medicine_enzyme'] = last_element_dic
                            partner_list.append(partner_dict)

                    else:
                        medicine_enzyme = str(line.split()[3:]).replace("['",'').replace("']",'').strip()

                        partner_dict['medicine_enzyme'] = medicine_enzyme
                        partner_list.append(partner_dict)

                ddi['partner'] = partner_list

                json.dump(ddi, open(save_dir + drugID_1 + '.json', 'w'), ensure_ascii=False, indent=4)


def main():
    index_dir = '/home/cqfnenu/nosql-biosets-master/keggdrug/ddi_data/'
    save_dir = '/home/cqfnenu/nosql-biosets-master/keggdrug/ddi_json/'
    parse_ddi_file(index_dir, save_dir)


################################################################################################################
if __name__ == '__main__':
    main()
