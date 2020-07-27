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

    # -----------------------------------------------------------------------------------------------------------
    # 获取Expression Data表格
    expression_table = soup.find_all('table', attrs={"style": "text-align:center; margin-left:20pt", "border": "1"})
    print(len(expression_table))
    link_1 = []
    link_2 = []
    link_3 = []
    link_4 = []

    for each in expression_table:
        get_a = each.find_all('a')
        for each in get_a:
            get_link = each.get('href')
            element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
            link_1.append(element_col[0])
        Organ_link = link_1[::2]    # 取奇数位上的值
        Source_link = link_1[1::2]  # 取偶数位

    expression_link = pd.DataFrame({'Organ_link': Organ_link, 'Source_link': Source_link})
    print(expression_link)

    # [0]:表示第一个table,多个table需要指定,如果不指定默认第一个,如果没有[0],输入dataframe格式组成的list
    df = pd.read_html(str(expression_table))[0]
    df_bigger = pd.concat([df, expression_link], axis=1)
    df_bigger.to_csv(new_dir + 'expression.csv', index=False)

    # ----------------------------------------------------------------------------------------------------------
    # 获取Substrates、Inhibitors、Drug-Drug Interactions三个表格
    tables_content = soup.find_all('table', attrs={"style": "text-align:center; margin-left:20pt; font-family:verdana",
    "border": "1"})
    print(len(tables_content))

    if len(tables_content) == 3:
        # 获取Substrate信息及链接
        for each in tables_content[0].find_all('tr'):

            get_a = each.find_all('a')
            for each in get_a:
                get_link = each.get('href')
                element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                link_2.append(element_col[0])
            Substrate_link = link_2[::2]  # 取奇数位上的值
            Reference_link = link_2[1::2]  # 取偶数位

        # 保存substrates
        substrates_link = pd.DataFrame({'Substrate_link': Substrate_link, 'Reference_link': Reference_link})
        df_1 = pd.read_html(str(tables_content))[0]
        df_bigger_1 = pd.concat([df_1, substrates_link], axis=1)
        df_bigger_1.to_csv(new_dir + 'substrates.csv', index=False)

        # -----------------------------------------------------------------------------------------------------------
        # 获取Inhibitors信息及链接
        for each in tables_content[1].find_all('tr'):
            get_a = each.find_all('a')
            for each in get_a:
                get_link = each.get('href')
                element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                link_3.append(element_col[0])
            print(len(link_3))
            Inhibitor_link = []
            Substrate_used_link = []
            Reference_link = []
            for i in range(len(link_3)):
                if i % 3 == 0:
                    Inhibitor_link.append(link_3[i])
                elif i % 3 == 1:
                    Substrate_used_link.append(link_3[i])
                elif i % 3 == 2:
                    Reference_link.append(link_3[i])

        # 保存inhibitors
        inhibitors_link = pd.DataFrame({'Inhibitor_link': Inhibitor_link, 'Substrate_used_link': Substrate_used_link,
                                        'Reference_link': Reference_link})
        df_2 = pd.read_html(str(tables_content))[1]
        df_bigger_2 = pd.concat([df_2, inhibitors_link], axis=1)
        df_bigger_2.to_csv(new_dir + 'inhibitors.csv', index=False)

        # -----------------------------------------------------------------------------------------------------------
        # 获取DDI信息及链接
        for each in tables_content[2].find_all('td'):
            get_a = each.find_all('a')
            a_element = []

            if len(get_a) == 2:
                for each in get_a:
                    get_link = each.get('href')
                    element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                    a_element.append(element_col)
                link_4.append(a_element)

            else:
                for each in get_a:
                    get_link = each.get('href')
                    element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                    link_4.append(element_col[0])

            print(len(link_4))
            Interacting_Drug_link = []
            Affected_Drug_link = []
            Reference_link = []
            DDI_link = []
            for i in range(len(link_4)):
                if i % 4 == 0:
                    Interacting_Drug_link.append(link_4[i])
                elif i % 4 == 1:
                    Affected_Drug_link.append(link_4[i])
                elif i % 4 == 2:
                    Reference_link.append(link_4[i])
                elif i % 4 == 3:
                    DDI_link.append(link_4[i])

        # 保存ddi
        ddi_link = pd.DataFrame({'Interacting_Drug_link': Interacting_Drug_link, 'Affected_Drug_link': Affected_Drug_link,
                                        'Reference_link': Reference_link, 'DDI_link': DDI_link})
        df_3 = pd.read_html(str(tables_content))[2]
        df_bigger_3 = pd.concat([df_3, ddi_link], axis=1)
        df_bigger_3.to_csv(new_dir + 'ddi.csv', index=False)


    else:
        # 获取Substrate信息及链接
        for each in tables_content[0].find_all('tr'):

            get_a = each.find_all('a')
            for each in get_a:
                get_link = each.get('href')
                element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                link_2.append(element_col[0])
            Substrate_link = link_2[::2]  # 取奇数位上的值
            Reference_link = link_2[1::2]  # 取偶数位

        # 保存substrates
        substrates_link = pd.DataFrame({'Substrate_link': Substrate_link, 'Reference_link': Reference_link})
        df_1 = pd.read_html(str(tables_content))[0]
        df_bigger_1 = pd.concat([df_1, substrates_link], axis=1)
        df_bigger_1.to_csv(new_dir + 'substrates.csv', index=False)

        # -----------------------------------------------------------------------------------------------------------
        # 获取Inhibitors信息及链接
        for each in tables_content[1].find_all('tr'):
            get_a = each.find_all('a')
            for each in get_a:
                get_link = each.get('href')
                element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                link_3.append(element_col[0])
            print(len(link_3))
            Inhibitor_link = []
            Substrate_used_link = []
            Reference_link = []
            if len(link_3) / 3 == 0:
                for i in range(len(link_3)):
                    if i % 3 == 0:
                        Inhibitor_link.append(link_3[i])
                    elif i % 3 == 1:
                        Substrate_used_link.append(link_3[i])
                    elif i % 3 == 2:
                        Reference_link.append(link_3[i])
                # 保存inhibitors
                inhibitors_link = pd.DataFrame(
                    {'Inhibitor_link': Inhibitor_link, 'Substrate_used_link': Substrate_used_link,
                     'Reference_link': Reference_link})
                df_2 = pd.read_html(str(tables_content))[1]
                df_bigger_2 = pd.concat([df_2, inhibitors_link], axis=1)
                df_bigger_2.to_csv(new_dir + 'inhibitors.csv', index=False)

            else:
                Inhibitor_link = link_2[::2]  # 取奇数位上的值
                Reference_link = link_2[1::2]  # 取偶数位

                # 保存inhibitors
                inhibitors_link = pd.DataFrame({'Inhibitor_link': Inhibitor_link, 'Reference_link': Reference_link})
                df_2 = pd.read_html(str(tables_content))[1]
                df_bigger_2 = pd.concat([df_2, inhibitors_link], axis=1)
                df_bigger_2.to_csv(new_dir + 'inhibitors.csv', index=False)


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
