# 使用python爬取一个网页中表格的内容，并把抓取到的内容以json格式保存到文件中
"""
purpose:根据drug_id爬取整个网页表格
author:qiufen-chen
date:2020/07/07
"""
from bs4 import BeautifulSoup
import urllib.request
import unicodedata
from pprint import pprint
import json
import re

def check_link(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
        }
        # 发送请求并解析HTML对象
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        return html
    except:
        print('无法链接服务器！！！')


# 爬取资源
def get_contents(ulist, rurl):

    title = []    # 存表格第一列
    content = []  # 存表格第二列
    soup = BeautifulSoup(rurl, 'lxml')

    # 获取soup对象中所有属性为“class”属性值为“th50”或“th51”的th标签
    th_content = soup.findAll('th', attrs={"class": {'th50', 'th51'}})
    print(len(th_content))
    for i in range(0, len(th_content)):
        th_data = th_content[i].get_text()
        th_format = unicodedata.normalize('NFKC', th_data).strip()  # unicodedata.normalize()清理字符串,使用strip()居中对齐
        pprint(th_format)
        title.append(th_format)
    # print(title)

    # 获取soup对象中所有属性为“class”属性值为“td50”或“td51”的td标签
    td_content = soup.findAll('td', attrs={"class": {'td50', 'td51'}})
    print(len(td_content))
    for i in range(0, len(td_content)):
        td_data = td_content[i].get_text()
        td_format = unicodedata.normalize('NFKC', td_data).replace('\n', '').strip()   # 格式化并过滤掉'\n'
        content.append(td_format)
        # content.append(td_data)
        # pprint(td_format)
    # pprint(content)

    result_dic = dict(zip(title, content))

    if "Structure" in result_dic:
        del result_dic["Structure"]

    if "Brite" in result_dic:
        del result_dic["Brite"]

    if "LinkDB" in result_dic:
        del result_dic["LinkDB"]

    if "KCF data" in result_dic:
        del result_dic["KCF data"]

    if "Generic" in result_dic:
        del result_dic["Generic"]

    if "Product" in result_dic:
        del result_dic["Product"]

    if "Entry" in result_dic:
        entry_value = result_dic["Entry"]
        new_entry_value = str(entry_value).split()[0]
        # pprint(new_entry_value)
        result_dic["Entry"] = new_entry_value

    if "Name" in result_dic:
        name_value = result_dic["Name"]
        new_name_value = str(name_value).split(';')
        result_dic["Name"] = new_name_value

    if "Remark" in result_dic:
        remark_value = result_dic["Remark"]
        new_remark_value = str(remark_value)
        remark_list = []
        remark_list.append(new_remark_value[0:15])

        # Convert to dictionary
        remark_dic = {}
        for i in range(len(remark_list)):
            remark_dic[remark_list[i].split(':')[0]] = remark_list[i].split(':')[1].strip()

        result_dic["Remark"] = remark_dic


    if "Other DBs" in result_dic:
        result_dic["LinkDB"] = result_dic.pop("Other DBs")  # 替换key值
        linkdb_value = result_dic["LinkDB"]
        new_linkdb_value = str(linkdb_value)
        linkdb_list = []
        linkdb_list.append(new_linkdb_value[0:14])
        linkdb_list.append(new_linkdb_value[14:30])
        linkdb_list.append(new_linkdb_value[30:42])
        linkdb_list.append(new_linkdb_value[42:63])
        linkdb_list.append(new_linkdb_value[63:90].strip())
        linkdb_list.append(new_linkdb_value[90:107])
        linkdb_list.append(new_linkdb_value[107:])
        pprint(linkdb_list)

        # Convert to dictionary
        linkdb_dic = {}
        for i in range(len(linkdb_list)):
            linkdb_dic[linkdb_list[i].split(':')[0]] = linkdb_list[i].split(':')[1].strip()
        result_dic["LinkDB"] = linkdb_dic

    # 使用json格式保存到文件中
    json.dump(result_dic, open('C:\\Users\\KerryChen\\Desktop\\nosql-biosets-master\\keggdrug\\D00001.json', 'w'), ensure_ascii=False, indent=4)


def main():

    urli = []
    url = 'https://www.kegg.jp/dbget-bin/www_bget?dr:D00001'
    rs = check_link(url)
    get_contents(urli, rs)

    # print(urli)


if __name__ == '__main__':
    main()






