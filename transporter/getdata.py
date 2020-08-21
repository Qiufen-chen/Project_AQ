#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/12 20:55
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : spider_ddi.py
# @Software: PyCharm
'''

from bs4 import BeautifulSoup
import urllib.request
from urllib import error
import time, os, re, json
import pprint
import pandas as pd


# ------------------------------------------------------------------------------------------------------------
def make_dir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + " Created folder sucessful!")
        return True
    else:
        print("This path is exist！")
        return False


# ------------------------------------------------------------------------------------------------------------
def check_link(url):
    # Send the request and parse the HTML object
    req = urllib.request.Request(url=url)
    try:
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")

        # Set sleep to 8, extend the wait time, and let the page load
        time.sleep(10)
        return html

    except error.HTTPError as e:
        print(e.code)
        return e.code


# ------------------------------------------------------------------------------------------------------------
def get_transporter_contents(rurl, tra_id):
    new_dir = '/home/cqfnenu/nosql-biosets-master/transporter/data/' + tra_id + '/'
    make_dir(new_dir)

    # Obtain Transporter's basic information
    soup = BeautifulSoup(rurl, 'lxml')
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

    # Get the Expression Data table
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
        Organ_link = link_1[::2]    # Take an odd number of values
        Source_link = link_1[1::2]  # Take the values in the even digits

    expression_link = pd.DataFrame({'Organ_link': Organ_link, 'Source_link': Source_link})
    print(expression_link)

    df = pd.read_html(str(expression_table))[0]
    df_bigger = pd.concat([df, expression_link], axis=1)
    df_bigger.to_csv(new_dir + 'expression.csv', index=False)

    # Obtain Substrates, Inhibitors and drug-drug Interactions in three tables
    tables_content = soup.find_all('table', attrs={"style": "text-align:center; margin-left:20pt; font-family:verdana",
    "border": "1"})
    print(len(tables_content))

    if len(tables_content) == 3:
        # Obtain Substrate information and links
        for each in tables_content[0].find_all('tr'):
            get_a = each.find_all('a')

            for each in get_a:
                get_link = each.get('href')
                element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                link_2.append(element_col[0])
            Substrate_link = link_2[::2]
            Reference_link = link_2[1::2]

        # Preserve substrates information
        substrates_link = pd.DataFrame({'Substrate_link': Substrate_link, 'Reference_link': Reference_link})
        df_1 = pd.read_html(str(tables_content))[0]
        df_bigger_1 = pd.concat([df_1, substrates_link], axis=1)
        df_bigger_1.to_csv(new_dir + 'substrates.csv', index=False)


        # Obtain Inhibitors information and links
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

        # Preserve inhibitors information
        inhibitors_link = pd.DataFrame({'Inhibitor_link': Inhibitor_link, 'Substrate_used_link': Substrate_used_link,
                                        'Reference_link': Reference_link})
        df_2 = pd.read_html(str(tables_content))[1]
        df_bigger_2 = pd.concat([df_2, inhibitors_link], axis=1)
        df_bigger_2.to_csv(new_dir + 'inhibitors.csv', index=False)

        # Get DDI information and links
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

        # Save the DDI information
        ddi_link = pd.DataFrame({'Interacting_Drug_link': Interacting_Drug_link, 'Affected_Drug_link': Affected_Drug_link,
                                 'Reference_link': Reference_link, 'DDI_link': DDI_link})
        df_3 = pd.read_html(str(tables_content))[2]
        df_bigger_3 = pd.concat([df_3, ddi_link], axis=1)
        df_bigger_3.to_csv(new_dir + 'ddi.csv', index=False)


    else:
        # Obtain Substrate information and links
        for each in tables_content[0].find_all('tr'):
            get_a = each.find_all('a')

            for each in get_a:
                get_link = each.get('href')
                element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                link_2.append(element_col[0])
            Substrate_link = link_2[::2]
            Reference_link = link_2[1::2]

        # Preserve substrates information
        substrates_link = pd.DataFrame({'Substrate_link': Substrate_link, 'Reference_link': Reference_link})
        df_1 = pd.read_html(str(tables_content))[0]
        df_bigger_1 = pd.concat([df_1, substrates_link], axis=1)
        df_bigger_1.to_csv(new_dir + 'substrates.csv', index=False)

        # Obtain Inhibitors information and links
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

                # Preserve inhibitors information
                inhibitors_link = pd.DataFrame(
                    {'Inhibitor_link': Inhibitor_link, 'Substrate_used_link': Substrate_used_link,
                     'Reference_link': Reference_link})
                df_2 = pd.read_html(str(tables_content))[1]
                df_bigger_2 = pd.concat([df_2, inhibitors_link], axis=1)
                df_bigger_2.to_csv(new_dir + 'inhibitors.csv', index=False)

            else:
                Inhibitor_link = link_2[::2]
                Reference_link = link_2[1::2]

                # Preserve inhibitors information
                inhibitors_link = pd.DataFrame({'Inhibitor_link': Inhibitor_link, 'Reference_link': Reference_link})
                df_2 = pd.read_html(str(tables_content))[1]
                df_bigger_2 = pd.concat([df_2, inhibitors_link], axis=1)
                df_bigger_2.to_csv(new_dir + 'inhibitors.csv', index=False)


# ------------------------------------------------------------------------------------------------------------
# Get compound information
def get_compound_contents(rurl, com_id ):
    new_dir = '/home/cqfnenu/nosql-biosets-master/transporter/compounds_data/' + com_id + '/'
    make_dir(new_dir)
    soup = BeautifulSoup(rurl, 'lxml')
    link_5 = []
    link_6 = []
    link_7 = []

    # Obtain Substrates, Inhibitors and drug-drug Interactions in three tables
    tables_content = soup.find_all('table', attrs={"style": "text-align:center; margin-left:20pt; font-family:verdana",
                                                   "border": "1"})
    print(len(tables_content))

    if len(tables_content) == 2:
        for i in range(0, len(tables_content)):

            df = pd.read_html(str(tables_content))[i]

            # Get the column name through df.columns.values
            # Convert it to a list through df.columns..tolist() or list(df.columns)
            colNames_List = df.columns.values.tolist()
            print(colNames_List)

            if 'Inhibitor' in colNames_List:

                # Access Inhibitors information and links
                for each in tables_content[i].find_all('tr'):
                    get_a = each.find_all('a')
                    for each in get_a:
                        get_link = each.get('href')
                        element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                        link_5.append(element_col[0])
                    print(len(link_5))

                    Transporter_link = []
                    Inhibitor_link = []
                    Substrate_used_link = []
                    Reference_link = []

                    for i in range(len(link_5)):
                        if i % 4 == 0:
                            Transporter_link.append(link_5[i])
                        elif i % 4 == 1:
                            Inhibitor_link.append(link_5[i])
                        elif i % 4 == 2:
                            Substrate_used_link.append(link_5[i])
                        elif i % 4 == 3:
                            Reference_link.append(link_5[i])

                # Preserve inhibitors information
                inhibitors_link = pd.DataFrame({'Transporter_link': Transporter_link, 'Inhibitor_link': Inhibitor_link,
                                                'Substrate_used_link': Substrate_used_link, 'Reference_link': Reference_link})
                df_bigger_1 = pd.concat([df, inhibitors_link], axis=1)
                df_bigger_1.to_csv(new_dir + 'inhibitors.csv', index=False)


            elif ('DDI', 'DDI') in colNames_List:

                # Get DDI information and links
                for each in tables_content[i].find_all('td'):
                    get_a = each.find_all('a')
                    a_element = []

                    if len(get_a) == 2:
                        for each in get_a:
                            get_link = each.get('href')
                            element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                            a_element.append(element_col)
                        link_6.append(a_element)

                    else:
                        for each in get_a:
                            get_link = each.get('href')
                            element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                            link_6.append(element_col[0])
                    print(len(link_6))

                    Interacting_Drug_link = []
                    Affected_Drug_link = []
                    Reference_link = []
                    DDI_link = []

                    for i in range(len(link_6)):
                        if i % 4 == 0:
                            Interacting_Drug_link.append(link_6[i])
                        elif i % 4 == 1:
                            Affected_Drug_link.append(link_6[i])
                        elif i % 4 == 2:
                            Reference_link.append(link_6[i])
                        elif i % 4 == 3:
                            DDI_link.append(link_6[i])

                # Save the DDI information
                ddi_link = pd.DataFrame(
                    {'Interacting_Drug_link': Interacting_Drug_link, 'Affected_Drug_link': Affected_Drug_link,
                     'Reference_link': Reference_link, 'DDI_link': DDI_link})

                df_bigger_2 = pd.concat([df, ddi_link], axis=1)
                df_bigger_2.to_csv(new_dir + 'ddi.csv', index=False)

            else:
                # Obtain Substrate information and links
                for each in tables_content[i].find_all('tr'):
                    get_a = each.find_all('a')

                    for each in get_a:
                        get_link = each.get('href')
                        element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                        link_7.append(element_col[0])
                    Transporter_link = link_7[::2]
                    Reference_link = link_7[1::2]

                # Preserve substrates information
                substrates_link = pd.DataFrame({'Transporter_link': Transporter_link, 'Reference_link': Reference_link})
                df_bigger_3 = pd.concat([df, substrates_link], axis=1)
                df_bigger_3.to_csv(new_dir + 'substrates.csv', index=False)
                df.to_csv(new_dir + 'substrates.csv', index=False)

    elif len(tables_content) == 1:
        df = pd.read_html(str(tables_content))[0]
        colNames_List = df.columns.values.tolist()
        print(colNames_List)

        if 'Inhibitor' in colNames_List:
            # Access Inhibitors information and links
            for each in tables_content[0].find_all('tr'):
                get_a = each.find_all('a')
                for each in get_a:
                    get_link = each.get('href')
                    element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                    link_5.append(element_col[0])
                print(len(link_5))

                Transporter_link = []
                Inhibitor_link = []
                Substrate_used_link = []
                Reference_link = []
                for i in range(len(link_5)):
                    if i % 4 == 0:
                        Transporter_link.append(link_5[i])
                    elif i % 4 == 1:
                        Inhibitor_link.append(link_5[i])
                    elif i % 4 == 2:
                        Substrate_used_link.append(link_5[i])
                    elif i % 4 == 3:
                        Reference_link.append(link_5[i])

            # Preserve inhibitors information
            inhibitors_link = pd.DataFrame({'Transporter_link': Transporter_link, 'Inhibitor_link': Inhibitor_link,
                                            'Substrate_used_link': Substrate_used_link,
                                            'Reference_link': Reference_link})
            df_bigger_1 = pd.concat([df, inhibitors_link], axis=1)
            df_bigger_1.to_csv(new_dir + 'inhibitors.csv', index=False)

        elif ('DDI', 'DDI') in colNames_List:

            # Get DDI information and links
            for each in tables_content[0].find_all('td'):
                get_a = each.find_all('a')
                a_element = []

                if len(get_a) == 2:
                    for each in get_a:
                        get_link = each.get('href')
                        element_col = get_link.replace('\n', ',').replace('../../','http://transportal.compbio.ucsf.edu/').split(',')
                        a_element.append(element_col)
                    link_6.append(a_element)

                else:
                    for each in get_a:
                        get_link = each.get('href')
                        element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                        link_6.append(element_col[0])
                print(len(link_6))

                Interacting_Drug_link = []
                Affected_Drug_link = []
                Reference_link = []
                DDI_link = []

                for i in range(len(link_6)):
                    if i % 4 == 0:
                        Interacting_Drug_link.append(link_6[i])
                    elif i % 4 == 1:
                        Affected_Drug_link.append(link_6[i])
                    elif i % 4 == 2:
                        Reference_link.append(link_6[i])
                    elif i % 4 == 3:
                        DDI_link.append(link_6[i])

            # Save the DDI information
            ddi_link = pd.DataFrame(
                {'Interacting_Drug_link': Interacting_Drug_link, 'Affected_Drug_link': Affected_Drug_link,
                 'Reference_link': Reference_link, 'DDI_link': DDI_link})

            df_bigger_2 = pd.concat([df, ddi_link], axis=1)
            df_bigger_2.to_csv(new_dir + 'ddi.csv', index=False)

        else:
            for each in tables_content[0].find_all('tr'):
                get_a = each.find_all('a')
                for each in get_a:
                    get_link = each.get('href')
                    element_col = get_link.replace('\n', ',').replace('../../', 'http://transportal.compbio.ucsf.edu/').split(',')
                    link_7.append(element_col[0])
                Transporter_link = link_7[::2]  # Take an odd number of values
                Reference_link = link_7[1::2]  # Take the values in the even digits

            # Preserve substrates information
            substrates_link = pd.DataFrame({'Transporter_link': Transporter_link, 'Reference_link': Reference_link})
            df_bigger_3 = pd.concat([df, substrates_link], axis=1)
            df_bigger_3.to_csv(new_dir + 'substrates.csv', index=False)
            df.to_csv(new_dir + 'substrates.csv', index=False)

    else:
        print("There is nothing to crawl here")


# ------------------------------------------------------------------------------------------------------------
def main():
    transporter_path = '/home/cqfnenu/nosql-biosets-master/transporter/transporters_index.txt'
    with open(transporter_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            str_line = str(line.split('(')[0]).rstrip()
            url = 'http://transportal.compbio.ucsf.edu/transporters/' + str_line
            pprint.pprint(url)
            rs = check_link(url)
            get_transporter_contents(rs, str_line)
            print('{} successful crawl!'.format(str_line))

    compound_path = '/home/cqfnenu/nosql-biosets-master/transporter/compounds_index.txt'
    with open(compound_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() != "":  # Check that the row is not empty
                str_line = line.lower().replace(' ', '-').replace('/', '-').replace(',','_').rstrip()
                url = 'http://transportal.compbio.ucsf.edu/compounds/' + str_line
                pprint.pprint(url)
                rs = check_link(url)
                get_compound_contents(rs, str_line)
                print('{} successful crawl!'.format(str_line))


# ------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
