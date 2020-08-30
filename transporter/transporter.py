#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/21 23:16
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : transporter.py
# @Software: PyCharm
'''


""" Index Transporter json datasets with MongoDB"""

import json
import os
import argparse
from utils.dbutils import DBconnection
import sys

sys.path.append(os.path.abspath(__file__).rsplit('/', 2)[0])

DOCTYPE = 'transpoter'


# ---------------------------------------------------------------------------------------------------
def main(infile_path, index, doctype=DOCTYPE, host=None, port=None):
    if not infile_path:
        #  Gets the full path to the script
        file_path = os.path.abspath(__file__).rsplit('/', 2)[0] + "/transporters_json/"
    else:
        file_path = infile_path
    print(file_path)

    db_transportal = DBconnection(index, host=host, port=port)

    for (root, dirs, files) in os.walk(file_path):
        for filename in files:

            if doctype in ['transporter', 'compound']:
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    tran_data = json.load(f)
                    db_transportal.mdbi[doctype].insert(tran_data)
                print(filename + " insert successfully!")

            else:
                pass


#########################################################################################################################################
if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Index Transportal JSON dataset with MongoDB')
    # parser.add_argument('-infile',
    #                     '--infile',
    #                     help='Input folder name')
    # parser.add_argument('--index',
    #                     default="all",
    #                     help='Name of the MongoDB database index')
    # parser.add_argument('--mdbcollection',
    #                     default=DOCTYPE,
    #                     help='MongoDB collection name')
    # parser.add_argument('--host',
    #                     help='MongoDB server hostname')
    # parser.add_argument('--port',
    #                     help="MongoDB server port number")
    #
    # args = parser.parse_args()
    # main(args.infile, args.index, args.mdbcollection, args.host, args.port)

    # ------------------------------------------------------------------------------------------------------------------------------------
    # Transporter data to MongoDB
    main('/home/cqfnenu/nosql-biosets-master/transporter/transporters_json/', 'transportal', 'transporter', '39.97.240.2')

    # Compound data to MongoDB
    main('/home/cqfnenu/nosql-biosets-master/transporter/compounds_json/', 'transportal', 'compound', '39.97.240.2')

