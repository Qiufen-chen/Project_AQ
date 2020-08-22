#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/21 23:14
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : keggdrug.py
# @Software: PyCharm
'''

# from pymongo import MongoClient
# import json
# import os
# import argparse
#
#
# # ---------------------------------------------------------------------------------------------------
# def connection(host, password, user, mdbdb, doctype):
#
#     conn = MongoClient(host)
#     db_signin = conn['admin']
#     db_signin.authenticate(user, password)
#     db = conn[mdbdb]
#     set = db[doctype]
#     return set
#
#
# # ---------------------------------------------------------------------------------------------------
# def insertToMongoDB(set, jsondir, doctype):
#
#     for (root, dirs, files) in os.walk(jsondir):
#         for filename in files:
#
#             if doctype == "drug":
#                 with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
#                     drug_data = json.load(f)
#                     set.insert(drug_data)
#                 print(filename + " insert successfully!")
#
#             if doctype == 'interaction':
#                 with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
#                     ddi_data = json.load(f)
#                     set.insert(ddi_data)
#                 print(filename + " insert successfully!")
#
#
# # ---------------------------------------------------------------------------------------------------
# def main(dir, mdbdb, doctype, host, user, password):
#     """
#     Index KEGGDrug json dataset with MongoDB
#     :param dir: Input dir pathway
#     :param mdbdb: Name of the MongoDB database, default=ALL
#     :param doctype: MongoDB collection name, default=DOCTYPE
#     :param host: MongoDB server host name
#     :param user: User login name
#     :param password: MongoDB server password
#     :return:
#     """
#
#     set = connection(host, password, user, mdbdb, doctype)
#     insertToMongoDB(set, dir, doctype)
#
#
# #########################################################################################################################################
# if __name__ == '__main__':
#
#     # parser = argparse.ArgumentParser(description='Index KEGGDrug json dataset with MongoDB')
#     # parser.add_argument('--dir', required=True, help='Input dir pathway')
#     # parser.add_argument('--mdbdb', help='Name of the MongoDB database index')
#     # parser.add_argument('--doctype', help='MongoDB collection name')
#     # parser.add_argument('--host', help='MongoDB server host name')
#     # parser.add_argument('--user', help='User login name')
#     # parser.add_argument('--password', help='MongoDB server password')
#     # args = parser.parse_args()
#     #
#     # main(args.dir, args.mdbdb, args.mdbcollection, args.host, args.user, args.password)
#
#     # ------------------------------------------------------------------------------------------------------------------------------------
#     # keggdrug_drug data to MongoDB
#     # main('/home/cqfnenu/nosql-biosets-master/keggdrug/drug_json/', 'keggdrug', 'drug', '39.97.240.2', 'root', "@nenu_icb_2019_2022@")
#
#     # keggdrug_ddi data to MongoDB
#     main('/home/cqfnenu/nosql-biosets-master/keggdrug/ddi_json/', 'keggdrug', 'interaction', '39.97.240.2', 'root', "@nenu_icb_2019_2022@")



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



#########################################################################################################################################

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
