"""
purpose:批量爬取transporters数据
author:qiufen-chen
date:2020/07/13
"""

from bs4 import BeautifulSoup
import urllib.request
from urllib import error
import time, os, re, json
import pprint
import pandas as pd


def make_dir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + " Created folder sucessful!")
        return True
    else:
        print("This path is exist！")
        return False


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
def get_contents(rurl, tra_id):
    new_dir = '/home/cqfnenu/nosql-biosets-master/transporter/data/' + tra_id + '/'
    make_dir(new_dir)
    soup = BeautifulSoup(rurl, 'lxml')

    # -----------------------------------------------------------------------------------------------------------
    # 获取Transporter基本信息
    basic_info = soup.find_all('p', attrs={'style': 'margin-left:20pt'})

    list = []
    for each in basic_info:
        br = str(each).replace('<br/>', '\n')
        p_content = re.sub(u"\\<.*?\\>", " ", br).replace('Entrez Gene Link', '').replace(' ', '').rstrip()
        element = str(p_content.split(':')[1]).split(',')
        list.append(element)

        get_a = each.find_all('a')
        for each in get_a:
            get_link = each.get('href')

        df = pd.DataFrame({'Synonyms': list, 'Entrez Gene Link': get_link})
        df.to_csv(new_dir + 'basic_information.csv', index=False)


def main(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            str_line = str(line.split('(')[0]).rstrip()
            url = 'http://transportal.compbio.ucsf.edu/transporters/' + str_line
            pprint.pprint(url)
            rs = check_link(url)
            get_contents(rs, str_line)
            print('{} 成功爬取!'.format(str_line))


if __name__ == '__main__':
    path = '/home/cqfnenu/nosql-biosets-master/transporter/transporters_index.txt'
    main(path)
