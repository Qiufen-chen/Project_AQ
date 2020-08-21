"""
从大到小的思路：
1.产生不同的页码的链接
2.每个链接，先获取网页源代码
3.每个页面内，先抓全部的 Entry字段
5.最终结果保存到 txt文件中
"""
# ——————————————————————————————————————————————————————————————————————————————————————————————————————
"""
purpose:找到数据库中的所有药物id的list
author:qiufen-chen
date:2020/06/20
"""
# ——————————————————————————————————————————————————————————————————————————————————————————————————————
import requests
import re
import time

class get_drugId(object):

    def __init__(self):
        print(u'Please wait while we begin to crawl the contents')


    # 'changepage' is used to produce links from different pages
    def changepage(self, url, total_page):

        now_page = int(re.search('page=(\d+)', url, re.S).group(1))
        for i in range(now_page, total_page + 1):
            link = re.sub('page=\d+', 'page=%s' % i, url, re.S)
        return link


    # 'getsource' is used to get the web page source code
    def getsource(self, url):
        time.sleep(8)
        html = requests.get(url)
        return html.text


    # 'geteveryentry' is used to grab the information for each entry
    def geteveryentry(self, source):
        everyentry = re.findall('(<td class="data1">(.*?)</td>)', source, re.S)  # 查找所有td标签里的内容
        # print(everyentry)
        return everyentry


    # 'getinfo' is used to extract the information we need for Entry from each 'td'
    def getinfo(self, eachclass):
        info = {}
        entry_list = re.findall('<a.*?>(.*?)</a>', str(eachclass), re.S)
        if len(entry_list) == 2:
            info['entry_id'] = entry_list[0]
            print(info)
        return info

    # 'saveinfo' is used to save the results to the KeggDrug_entry.txt file
    def saveinfo(self, classinfo):
        f = open('C:\\Users\\KerryChen\\Desktop\\nosql-biosets-master\\KeggDrug_Data\\KeggDrug_entry.txt', 'a')
        for each in classinfo:
            if 'entry_id' in each:
                f.write(str(each['entry_id']) + '\n')
        f.close()


if __name__ == '__main__':
    classinfo = []  # 存放最终结果
    url = 'https://www.kegg.jp/kegg-bin/search?display=drug&target=compound%2bdrug%2bdgroup%2benviron%2bdisease&uid=159264126976624&search_gene=1&page=1&from=drug'
    Keggspider = get_drugId()
    all_links = Keggspider.changepage(url, 282)  # 产生不同的页码的链接

    for link in all_links:
        print(u'正在处理页面：' + link)
        html = Keggspider.getsource(link)  # 每个链接，先获取网页源代码
        everyclass = Keggspider.geteveryentry(html)  # 每个页面内，先抓每个Entry的版块
        for each in everyclass:
            # print(each)
            info = Keggspider.getinfo(each)  # 每个Entry版块内，抓Entry_ID存到字典里
            classinfo.append(info)
            # print(classinfo)
    Keggspider.saveinfo(classinfo)  # 最终结果保存到txt文件中

    print('The drug_IDs were successfully obtained!')
