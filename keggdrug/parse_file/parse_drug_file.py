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


from pprint import pprint
import json
import os
import argparse
from utils.dbutils import DBconnection
import sys
sys.path.append(os.path.abspath(__file__).rsplit('/', 2)[0])
DOCTYPE = 'keggdrug'



class parse_file():

    @staticmethod
    def process_drug_file(file_path):  # 脚本文件所在的路径
        index_path = file_path + '/dataset/drug_file/drug'
        save_path = file_path + '/dataset/drug_data/'

        with open(os.path.join(index_path), 'r', encoding='utf-8') as file:
            drug_list = []
            for line in file:
                drug_list.append(line)

            str_index = [index for (index, value) in enumerate(drug_list) if value == '///\n']

            for i in range(len(str_index)-1):
                element_list = [drug_list[j] for j in range(str_index[i], str_index[i+1])]

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

    @staticmethod
    def parse_ddi_file(file_path):

        ddi_dic = {}
        drug_id = str(file_path.split('/')[-1]).split('.')[0]
        print(drug_id)
        ddi_dic["DRUG_ID"] = drug_id
        with open(file_path, 'r', encoding='utf-8') as f:

            lines = f.readlines()
            partner_list = []

            for line in lines:
                partner_dict = {}

                partner_dict["DRUG_ID"] = str(line.split()[1]).split(':')[1].strip()

                partner_dict['STATISTICAL_PARAMETER'] = line.split()[2].strip()

                partner_dict['MEDICINE_ENZYME'] = {}
                if line.find('CI') != -1:
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
                    new_line = line[line.find('P') + 1:].strip()
                    if '/' in new_line and ':' in new_line:
                        element_list = new_line.replace('\t', '').replace('\n', '').split('/')
                        pprint(element_list)
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

        ddi_dic['PARTNER'] = partner_list
        return ddi_dic

    @staticmethod
    def parse_drug_file(file_path):

        drug_index_path = file_path + '/dataset/drug_data/'
        ddi_index_path = file_path + '/dataset/ddi_data/'
        drug_save_path = file_path + '/dataset/drug_json/'

        entry_list = ['FORMULA', 'EXACT_MASS', 'MOL_WEIGHT', 'EFFICACY', 'TYPE',
                      'COMMENT', 'TARGET', 'COMPONENT', 'SEQUENCE']

        for (drug_root, drug_dirs, drug_files) in os.walk(drug_index_path):
            for file_name in drug_files:
                drug_dic = {}
                with open(os.path.join(drug_root, file_name), 'r', encoding='utf-8') as file:
                    for line in file:
                        new_line = line[0:12].strip()

                        if new_line == 'ENTRY':
                            drug_id = line[12:20].strip()
                            drug_dic['DRUG_ID'] = line[12:20].strip()

                            for (ddi_root, ddi_dirs, ddi_files) in os.walk(ddi_index_path):
                                for filename in ddi_files:
                                    if str(filename).split('.')[0] == drug_id:
                                        print(filename)
                                        ddi_file_path = os.path.join(ddi_root, filename)
                                        ddi_dic = parse_file.parse_ddi_file(ddi_file_path)
                                        drug_dic['INTERACTION'] = ddi_dic['PARTNER']
                                    else:
                                        print('this is no such file')

                        if new_line in entry_list:
                            drug_dic[new_line] = line[12:].strip()

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

                    # pprint(drug_dic)
                    json.dump(drug_dic, open(drug_save_path + drug_id + '.json', 'w'), ensure_ascii=False, indent=4)

    @staticmethod
    def parse_file_main():
        path = os.path.abspath(__file__).replace('\\', '/').rsplit('/', 2)[0]
        print(path)
        parse_file.process_drug_file(path)
        parse_file.parse_drug_file(path)

# ---------------------------------------------------------------------------------------------------------------------
def insertMongo(infile_path, index, doctype=DOCTYPE, host=None, port=None):

    if not infile_path:
        file_path = os.path.abspath(__file__).replace('\\', '').rsplit('/', 2)[0] + "/dataset/drug_json/"
    else:
        file_path = infile_path
    print(file_path)

    db_keggdrug = DBconnection(index, host=host, port=port)
    pprint(db_keggdrug)
    for (root, dirs, files) in os.walk(file_path):
        for filename in files:
            if doctype == 'drug':
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    db_keggdrug.mdbi["drug"].insert_one(data)
                print(filename + " insert successfully!")


# ---------------------------------------------------------------------------------------------------------------------
def main(infile_path, index, doctype):
    parse_file.parse_file_main()
    insertMongo(infile_path, index, doctype, host=None, port=None)


# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    d = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description='Index KEGGDrug JSON dataset with MongoDB')
    parser.add_argument('-infile',
                        '--infile',
                        help='Input folder path')
    parser.add_argument('--index',
                        default="all",
                        help='Name of the MongoDB database index')
    parser.add_argument('--mdbcollection',
                        default=DOCTYPE,
                        help='MongoDB collection name')
    parser.add_argument('--host',
                        help='MongoDB server hostname')
    parser.add_argument('--port',
                        help="MongoDB server port number")

    args = parser.parse_args()
    main(args.infile, args.index, args.mdbcollection, args.host, args.port)

    # ------------------------------------------------------------------------------------------------------------------------------------
    # keggdrug_drug data to MongoDB
    # main('/home/cqfnenu/nosql-biosets-master/keggdrug/dataset/drug_json/', 'keggdrug', 'drug')






