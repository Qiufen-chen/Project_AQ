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

class spider(object):

    def __init__(self):
        print(u'正在开始爬取内容，请稍等')

    # changepage用来生产不同页数的链接
    def changepage(self, url, total_page):
        # 使用re.search()扫描整个string查找匹配,会扫描整个字符串并返回第一个成功的匹配
        now_page = int(re.search('page=(\d+)', url, re.S).group(1))  # 使用re.S参数以后，正则表达式会将这个字符串作为一个整体，在整体中进行匹配。
        page_group = []
        for i in range(now_page, total_page + 1):
            link = re.sub('page=\d+', 'page=%s' % i, url, re.S)  # 使用re.sub(pattern, repl, string)将字符串中所有pattern用repel替换
            page_group.append(link)
        return page_group

    # getsource用来获取网页源代码
    def getsource(self, url):
        time.sleep(8)  # 将sleep设置为8，延长等待时间，让页面加载完毕
        html = requests.get(url)
        return html.text

    # geteveryentry用来抓取每个entry的信息
    def geteveryentry(self, source):
        everyentry = re.findall('(<td class="data1">(.*?)</td>)', source, re.S)  # 查找所有td标签里的内容
        # print(everyentry)
        return everyentry

    # getinfo用来从每个td中提取出我们需要Entry的信息
    def getinfo(self, eachclass):
        info = {}
        # 注意：re.findall()、re.search()、re.match()的区别，group(1) 会返回正则表达式中第一个括号内的内容
        entry_list = re.findall('<a.*?>(.*?)</a>', str(eachclass), re.S)  # 返回一个列表

        if len(entry_list) == 2:
            info['entry_id'] = entry_list[0]
            print(info)

        return info

    # saveinfo用来保存结果到KeggDrug_entry.txt文件中
    def saveinfo(self, classinfo):
        f = open('C:\\Users\\KerryChen\\Desktop\\nosql-biosets-master\\KeggDrug_Data\\KeggDrug_entry.txt', 'a')
        for each in classinfo:
            # 在读取dict的key和value时，如果key不存在，就会触发KeyError错误，因此用if做判断条件
            if 'entry_id' in each:
                f.write(str(each['entry_id']) + '\n')
        f.close()


if __name__ == '__main__':
    classinfo = []  # 存放最终结果
    url = 'https://www.kegg.jp/kegg-bin/search?display=drug&target=compound%2bdrug%2bdgroup%2benviron%2bdisease&uid=159264126976624&search_gene=1&page=1&from=drug'
    Keggspider = spider()
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

    print('Done!')
