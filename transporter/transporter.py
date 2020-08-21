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


from pymongo import MongoClient
import json
import os
import argparse


# ---------------------------------------------------------------------------------------------------
def connection(host, password, user, mdbdb, doctype):

    conn = MongoClient(host)
    db_signin = conn['admin']
    db_signin.authenticate(user, password)
    db = conn[mdbdb]
    set = db[doctype]
    return set


# ---------------------------------------------------------------------------------------------------
def insertToMongoDB(set, jsondir, doctype):

    for (root, dirs, files) in os.walk(jsondir):
        for filename in files:

            if doctype == "transporter":
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    tran_data = json.load(f)
                    set.insert(tran_data)
                print(filename + " insert successfully!")


            elif doctype == "compound":
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    comp_data = json.load(f)
                    set.insert(comp_data)
                print(filename + " insert successfully!")



# ---------------------------------------------------------------------------------------------------
def main(dir, mdbdb, doctype, host, user, password):
    """
    Index Transportal json dataset with MongoDB, downloaded from crawler
    :param dir: Input dir pathway
    :param mdbdb: Name of the MongoDB database, default=ALL
    :param doctype: MongoDB collection name, default=DOCTYPE
    :param host: MongoDB server host name
    :param user: User login name
    :param password: MongoDB server password
    :return:
    """

    set = connection(host, password, user, mdbdb, doctype)
    insertToMongoDB(set, dir, doctype)


#########################################################################################################################################
if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Index Transportal json dataset with MongoDB')
    # parser.add_argument('--dir', required=True, help='Input dir pathway')
    # parser.add_argument('--mdbdb', help='Name of the MongoDB database index')
    # parser.add_argument('--doctype', help='MongoDB collection name')
    # parser.add_argument('--host', help='MongoDB server host name')
    # parser.add_argument('--user', help='User login name')
    # parser.add_argument('--password', help='MongoDB server password')
    # args = parser.parse_args()
    #
    # main(args.dir, args.mdbdb, args.mdbcollection, args.host, args.user, args.password)

    # ------------------------------------------------------------------------------------------------------------------------------------
    # Transporter data to MongoDB
    # main('/home/cqfnenu/nosql-biosets-master/transporter/transporters_json/', 'transportal', 'transporter', '39.97.240.2', 'root', "@nenu_icb_2019_2022@")

    # Compound data to MongoDB
    main('/home/cqfnenu/nosql-biosets-master/transporter/compounds_json/', 'transportal', 'compound', '39.97.240.2', 'root', "@nenu_icb_2019_2022@")

