#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/13 09:32
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : parse_csv.py
# @Software: PyCharm
# @purpose : Python converts .CSV files into.JSON format files
'''

import pandas as pd
import json
import os
import argparse
from utils.dbutils import DBconnection

import importlib, sys
importlib.reload(sys)
sys.path.append(os.path.abspath(__file__).rsplit('/', 2)[0])


DOCTYPE = 'transpoter'


# ---------------------------------------------------------------------------------------------------
class parse_file():
    """ Batch parse of transporters_csv files and Compounds_csv files under XX path"""

    @staticmethod
    def parse_csv_file(dir_path, dir_name):
        # dir_path = os.path.abspath(__file__).replace('\\','/').rsplit('/', 2)[0] + '/dataset/transporters_csv/'
        # print(dir_path, dir_name)
        # save_path = os.path.abspath(__file__).rsplit('/', 2)[0] + '/dataset/' + dir_name + '/'
        # print(save_path)
        # print(dir_path)
        for (father_root, father_dirs, father_files) in os.walk(dir_path):
            print(father_root)
            for father_dir_name in father_dirs:
                # print(father_dir_name)
                element_dict = {}
                if dir_name == 'transporters_data':
                    element_dict = {'transporter_name': father_dir_name}
                    save_path = os.path.abspath(__file__).rsplit('/', 2)[0] + '/dataset/transporters_json/'
                    # print(save_path, element_dict)

                if dir_name == 'compounds_data':
                    element_dict = {'compound_name': father_dir_name}
                    save_path = os.path.abspath(__file__).rsplit('/', 2)[0] + '/dataset/compounds_json/'

                for (son_root, son_dirs, son_files) in os.walk(os.path.join(father_root, father_dir_name)):
                    for file_name in son_files:
                        str_file = str(file_name.split('.')[0])
                        path = os.path.join(son_root, file_name)

                        if os.path.isfile(path):

                            if str_file == 'basic_information':
                                data = pd.read_csv(path)
                                info_json = data.to_json(orient='records', force_ascii=False)
                                info_str = info_json.replace('[', '').replace(']', '').replace('\\', '').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                                info_result = eval(info_str)
                                element_dict['basic_information'] = info_result

                            if str_file == 'expression':
                                data = pd.read_csv(path)
                                exp_json = data.to_json(orient='records', force_ascii=False)
                                exp_str = exp_json.replace('[', '').replace(']', '').replace('\\', '').replace('null', 'None').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                                exp_result = eval(exp_str)
                                element_dict['expression'] = exp_result

                            if str_file == 'substrates':
                                data = pd.read_csv(path)
                                sub_json = data.to_json(orient='records', force_ascii=False)
                                sub_str = sub_json.replace('[', '').replace(']', '').replace('\\', '').replace('null','None').replace('\u03bc', 'μ').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                                sub_result = eval(sub_str)
                                element_dict['substrates'] = sub_result

                            if str_file == 'inhibitors':
                                data = pd.read_csv(path)
                                inh_json = data.to_json(orient='records', force_ascii=False)
                                inh_str = inh_json.replace('[', '').replace(']', '').replace('\u03bc', 'μ').replace('null','None').replace('\\', '').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                                inh_result = eval(inh_str)
                                element_dict['inhibitors'] = inh_result

                            if str_file == 'ddi':
                                data = pd.read_csv(path)

                                # Replace the header name
                                data.columns = ['DDI', 'Implicated Transporter', 'Interacting Drug', 'Affected Drug', 'AUC',
                                                'Cmax', 'CLR', 'CL/F', 't1/2', 'Effect on PD', 'Reference', 'More Details',
                                                'Interacting_Drug_link', 'Affected_Drug_link', 'Reference_link', 'DDI_link']

                                ddi_json = data.to_json(orient='records', force_ascii=False)

                                ddi_str = ddi_json.replace('[', '').replace(']', '').replace('\\', '').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')  # 可写成正则表达式

                                ddi_result = eval(ddi_str)

                                element_dict['drug_drug_interaction'] = ddi_result

                json.dump(element_dict, open(save_path + father_dir_name + '.json', 'w'), ensure_ascii=False, indent=4)

    @staticmethod
    def parse_file_main():
        transporter_dir = os.path.abspath(__file__).replace('\\','/').rsplit('/', 2)[0] + '/dataset/transporters_csv/'
        tran_dir_name = 'transporters_data'
        print(transporter_dir)

        parse_file.parse_csv_file(transporter_dir, tran_dir_name)

        compound_dir = os.path.abspath(__file__).replace('\\','/').rsplit('/', 2)[0] + '/dataset/compounds_csv/'
        cpd_dir_name = 'compounds_data'
        parse_file.parse_csv_file(compound_dir, cpd_dir_name)


# ---------------------------------------------------------------------------------------------------
def insertMongo(infile_path, index, doctype=DOCTYPE, host=None, port=None):

    db_transporter = DBconnection(index, host=host, port=port)

    for (root, dirs, files) in os.walk(infile_path):
        for filename in files:

            if doctype in ['transporter', 'compound']:
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    tran_data = json.load(f)
                    db_transporter.mdbi[doctype].insert(tran_data)
                print(filename + " insert successfully!")

            else:
                pass


# ---------------------------------------------------------------------------------------------------
def main(infile_path, index, doctype):
    # parse_file.parse_file_main()
    insertMongo(infile_path, index, doctype, host=None, port=None)


# ---------------------------------------------------------------------------------------------------
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Index Transportal JSON dataset with MongoDB')
#     parser.add_argument('-infile',
#                         '--infile',
#                         help='Input folder name')
#     parser.add_argument('--index',
#                         default="all",
#                         help='Name of the MongoDB database index')
#     parser.add_argument('--mdbcollection',
#                         default=DOCTYPE,
#                         help='MongoDB collection name')
#     # parser.add_argument('--host',
#     #                     help='MongoDB server hostname')
#     # parser.add_argument('--port',
#     #                     help="MongoDB server port number")
#
#     args = parser.parse_args()
#     main(args.infile, args.index, args.mdbcollection)

    # ------------------------------------------------------------------------------------------------------------------------------------
    # Transporter data to MongoDB
    insertMongo('/home/cqfnenu/nosql-biosets-master/transporter/dataset/transporters_json/', 'transporter', 'transporter')

    # Compound data to MongoDB
    main('/home/cqfnenu/nosql-biosets-master/transporter/dataset/compounds_json/', 'transporter', 'compound')



