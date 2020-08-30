#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/27 16:50
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : quries.py
# @Software: PyCharm
'''

""" Queries with KEGGDrug data indexed with MongoDB """

import arg
from utils.graphutils import *
from utils.dbutils import DBconnection
from utils.qryutils import parseinputquery, Query
# from utills.uniprot.query import QueryUniProt

db = "MongoDB"
DATABASE = "keggdrug"


class QueryDrugBank(Query):

    def autocomplete_drugnames(self, qterm, **kwargs):
        """
        Given partial drug names return possible names
        :param qterm: partial drug name
        :return: list of possible names
        """
        qc = {"$or": [
            {"NAME": {
                "$regex": "^%s" % qterm, "$options": "i"}}  # 正则表达式
        ]}
        # print(qc)
        cr = self.query(qc, projection=['NAME'], **kwargs)
        return cr

        # Target genes and interacted drugs

    def find_interacted_drugs(self, qc, limit=100):
        """
        Give a drug name return drug_interactions
        :param qc: drug name
        :param limit: 100
        :return: drug_interactions
        """
        aggqc = [
            {"$match": qc},  # drug_name
            {'$unwind': "$INTERACTION"},    # interactions
            {'$group': {
                '_id': {
                    'drug_id': '$DRUG_ID',
                    'drug': '$NAME',
                    'interactions_drug_id': '$INTERACTION.DRUG_ID'
                }}},
            {"$limit": limit}
        ]

        cr = self.aggregate_query(aggqc, allowDiskUse=True)

        r = []
        for i in cr:
            assert 'interactions_drug_id' in i['_id']
            ddi_id = i['_id']
            row = (ddi_id['drug_id'], ddi_id['drug'], ddi_id['interactions_drug_id'])
            r.append(row)
        return r


    def kegg_drug_id_to_drugbank_id(self, keggdid):
        """
        Given KEGG drug id return Drugbank drug id
        :param keggdid: KEGG drug id
        :return: Drugbank drug id
        """
        project = {"DBLINKS.DrugBank": 1}  # 使用投影操作符指定返回的键,查询时返回文档中所有键值
        qc = {"DRUG_ID": keggdid}
        r = list(self.query(qc, projection=project))
        assert 1 == len(r)
        return r[0]["_id"]








