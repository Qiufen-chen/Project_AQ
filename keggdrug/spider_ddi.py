#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/8/14 20:55
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : spider_ddi.py
# @Software: PyCharm
# @purpose : Batch crawl DDI data
'''


from bs4 import BeautifulSoup
import urllib.request
from urllib import error
import time


# --------------------------------------------------------------------------------------------------------
class get_ddi(object):

    # Send the request
    def check_link(self, url):
        req = urllib.request.Request(url=url)
        try:
            res = urllib.request.urlopen(req)
            html = res.read().decode("utf-8")
            time.sleep(8)  # Set sleep to 8, extend the wait time, and let the page load
            return html
        except error.HTTPError as e:
            print(e.code)
            return e.code


    # Get resources
    def get_ddi(self, rurl, drug_id):
        soup = BeautifulSoup(rurl, 'lxml')
        body_content = soup.findAll('body')
        print(len(body_content))
        for i in range(0, len(body_content)):
            pre_data = body_content[i].get_text()

            # Save as .txt file
            with open('C:/Users/KerryChen/Desktop/nosql-biosets-master/keggdrug/drug_json/' + str(drug_id).replace('\n', '') + '.txt', "w", encoding='utf-8') as f:
                f.write(pre_data)
                f.close()


def ddi_main():
    index_path = 'C:/Users/KerryChen/Desktop/nosql-biosets-master/keggdrug/drug_id.txt'
    with open(index_path, 'r') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            # print(line)
            i = i+1
            url = 'http://rest.kegg.jp/ddi/' + line  # API
            print(url)
            spider_ddi = get_ddi()
            rs = spider_ddi.check_link(url)
            if rs == 404:
                print('The page could not be found!')
            else:
                get_ddi(rs, line)
                print('第 {} 个网页成功爬取'.format(i))


if __name__ == '__main__':
    ddi_main()

