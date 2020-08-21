#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/21 23:12
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : parse_drug_file.py
# @Software: PyCharm
'''


""" Process drug data downloaded from FTP and parse it into JSON format"""

'''
Partial sample of drug data:
///
ENTRY       D06778            Crude     Drug
NAME        Pinellia tuber (JP17);
            Pineliae tuber (TN)
COMPONENT   3,4-Dihydroxybenzaldehyde [CPD:C16700]
SOURCE      Pinellia ternata [TAX:199225]
REMARK      Same as: E00148
            Therapeutic category: 5100
            Product: D06778<JP>
EFFICACY    Antiemetic, Antitussive, Expectorant, Sedative
COMMENT     Araceae (arum family) Pinellia tuber
            Major component: Homogentisic acid [CPD:C00544]
DBLINKS     PubChem: 47208429
'''


import os
from pprint import pprint
import json


def data_process(index_path, save_path):

    with open(os.path.join(index_path), 'r', encoding='utf-8') as file:
        drug_list = []
        for line in file:
            drug_list.append(line)

        str_index = [index for (index, value) in enumerate(drug_list) if value == '///\n']
        # pprint(str_index)

        for i in range(len(str_index)-1):
            element_list = []
            for j in range(str_index[i], str_index[i+1]):
                element_list.append(drug_list[j])

            # Delete the first element in the list：['///']
            element_list.pop(0)
            drug_id = element_list[0].split()[1]

            index = [index for (index, value) in enumerate(element_list) if str(value).startswith('ATOM')]
            if index:
                new_element_list = element_list[:index[0]]
                with open(save_path + drug_id + '.txt', 'w', encoding='utf-8') as f:
                    f.writelines(new_element_list)
                    f.close()
            else:
                with open(save_path + drug_id + '.txt', 'w', encoding='utf-8') as f:
                    f.writelines(element_list)
                    f.close()


def parse_drug(index_path, save_path):

    entry_list = ['FORMULA', 'EXACT_MASS', 'MOL_WEIGHT', 'EFFICACY', 'TYPE',
                  'COMMENT', 'TARGET', 'COMPONENT', 'SEQUENCE']

    for (root, dirs, files) in os.walk(index_path):
        for filename in files:
            drug_dic = {}

            with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                for line in file:
                    new_line = line[0:12].strip()

                    if new_line == 'ENTRY':
                        drug_id = line[12:20].strip()
                        drug_dic['DRUG_ID'] = line[12:20].strip()

                    if new_line in entry_list:
                        drug_dic[new_line] = line[12:].strip()

                    if new_line == 'EFFICACY':
                        drug_dic['EFFICACY'] = line[12:].strip()

                    # Gets the contents of the 'NAME' entry
                    if new_line == 'NAME':
                        name_list = []
                        while line:
                            name_list.append(line[10:].replace(';', '').strip())
                            line = file.readline()
                            pprint(line)
                            if line[0:12].strip() in entry_list:
                                break
                        drug_dic['NAME'] = name_list

                    # Gets the contents of the 'REMARK' entry
                    if new_line == 'REMARK':
                        remark_dic = {}
                        while line:
                            remark_dic[line[12:].split(':')[0].strip()] = line[12:].split(':')[1].strip()
                            line = file.readline()
                            # pprint(line)
                            if line[0:12].strip() in entry_list:
                                break
                        drug_dic['REMARK'] = remark_dic

                    # Gets the contents of the 'DBLINKS' entry
                    if new_line == 'DBLINKS':
                        dblink_dic = {}
                        while line:
                            dblink_dic[line[12:].split(':')[0].strip()] = line[12:].split(':')[1].strip()
                            line = file.readline()
                            # pprint(line)
                        drug_dic['DBLINKS'] = dblink_dic

                    if new_line == 'SEQUENCE':
                        while line:
                            line = file.readline()
                            if line[0:12].strip() in entry_list:
                                break

                    pprint(drug_dic)
                json.dump(drug_dic, open(save_path + drug_id + '.json', 'w'), ensure_ascii=False, indent=4)

def main():

    # The drug data is in the pathway
    index_drug_path = 'C:/Users/KerryChen/Desktop/nosql-biosets-master/keggdrug/drug_file/drug'

    # The drug data is stored after processing
    # save_drug_path = 'C:/Users/KerryChen/Desktop/nosql-biosets-master/keggdrug/drug_data/'
    save_drug_path = 'C:/Users/KerryChen/Desktop/nosql-biosets-master/keggdrug/11/'

    data_process(index_drug_path, save_drug_path)

    # -----------------------------------------------------------------------------------------
    # save_json_path = 'C:/Users/KerryChen/Desktop/nosql-biosets-master/keggdrug/drug_json/'
    # parse_drug(save_drug_path, save_json_path)


################################################################################################################
if __name__ == '__main__':
    main()
