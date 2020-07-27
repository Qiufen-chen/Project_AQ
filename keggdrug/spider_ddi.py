# 使用python爬取一个网页中body的内容，并把抓取到的内容保存到txt文件中
"""
purpose:批量爬取ddi数据
author:qiufen-chen
date:2020/07/08
"""

from bs4 import BeautifulSoup
import urllib.request
from urllib import error
import os
import time

def check_link(url):

    # 发送请求并解析HTML对象
    req = urllib.request.Request(url=url)
    try:
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        time.sleep(8)  # 将sleep设置为8，延长等待时间，让页面加载完毕
        return html
    except error.HTTPError as e:
        print(e.code)
        return e.code


# 爬取资源
def get_contents(rurl, drug_id):
    soup = BeautifulSoup(rurl, 'lxml')
    body_content = soup.findAll('body')
    print(len(body_content))
    for i in range(0, len(body_content)):
        pre_data = body_content[i].get_text()
        # 保存成txt格式
        with open('/home/cqfnenu/nosql-biosets-master/keggdrug/data/' + str(drug_id).replace('\n', '') + '.txt', "w", encoding='utf-8') as f:
        # with open('C:/Users/KerryChen/Desktop/nosql-biosets-master/keggdrug/data/' + str(drug_id).replace('\n','') + '.txt', "w", encoding='utf-8') as f:
            f.write(pre_data)
            f.close()

def main(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            # print(line)
            i = i+1
            url = 'http://rest.kegg.jp/ddi/'+ line
            print(url)
            rs = check_link(url)
            if rs == 404:
                pass
            else:
                get_contents(rs, line)
                print('第 {} 个网页成功爬取'.format(i))


# def main():
#     url = 'http://rest.kegg.jp/ddi/D00001'
#     rs = check_link(url)
#     # get_contents(rs)




if __name__ == '__main__':
    # path = 'C:\\Users\\KerryChen\\Desktop\\nosql-biosets-master\\keggdrug\\KeggDrug_entry.txt'
    path = '/home/cqfnenu/nosql-biosets-master/keggdrug/KeggDrug_entry.txt'
    main(path)
    # main()