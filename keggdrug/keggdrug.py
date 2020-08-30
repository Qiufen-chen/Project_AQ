#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/21 23:14
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : keggdrug.py
# @Software: PyCharm
'''


import json
import os
import argparse
from utils.dbutils import DBconnection
import sys
sys.path.append(os.path.abspath(__file__).rsplit('/', 2)[0])

DOCTYPE = 'keggdrug'

def main(infile_path, index, doctype=DOCTYPE, host=None, port=None):

    if not infile_path:
        file_path = os.path.abspath(__file__).rsplit('/', 2)[0] + "/drug_json/"
    else:
        file_path = infile_path
    print(file_path)

    db_keggdrug = DBconnection(index, host=host, port=port)

    for (root, dirs, files) in os.walk(file_path):
        for filename in files:

            if doctype == 'drug':
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    db_keggdrug.mdbi["drug"].insert_one(data)
                print(filename + " insert successfully!")



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
    # main('/home/cqfnenu/nosql-biosets-master/keggdrug/drug_json/', 'keggdrug', 'drug', '39.97.240.2')
