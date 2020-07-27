"""
purpose:python把.CSV文件转换成.JSON格式文件并格式化储存
author:qiufen-chen
date:2020/07/15
"""
import pandas as pd
import json
import os
import importlib, sys
importlib.reload(sys)


def main():

    # dir_path = '/home/cqfnenu/nosql-biosets-master/transporter/transporters_data/'
    dir_path = '/home/cqfnenu/nosql-biosets-master/transporter/compounds_data'
    # 遍历文件
    for (root_1, dirs_1, files_1) in os.walk(dir_path):
        for dir_name in dirs_1:

            drug_dict = {dir_name: ''}
            # 创建transports的字典
            # element_dict = {'basic information': '',
            #                 'expression': '',
            #                 'inhibitors': '',
            #                 'substrates': '',
            #                 'ddi': ''}
            # 创建compound的字典
            element_dict = {'inhibitors': '',
                            'substrates': '',
                            'ddi': ''}

            for (root_2, dirs_2, files_2) in os.walk(os.path.join(root_1, dir_name)):
                for file_name in files_2:
                    str_file = str(file_name.split('.')[0])
                    path = os.path.join(root_2, file_name)


                    if os.path.isfile(path):

                        if str_file == 'basic_information':
                            data = pd.read_csv(path)
                            info_json = data.to_json(orient='records', force_ascii=False)
                            info_result = eval(info_json.replace('[', '').replace(']', '').replace('\\', '')).replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                            element_dict['basic information'] = info_result

                        if str_file == 'expression':
                            data = pd.read_csv(path)
                            exp_json = data.to_json(orient='records', force_ascii=False)
                            exp_str = exp_json.replace('[', '').replace(']', '').replace('\\', '').replace('null', 'None').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                            exp_result = eval(exp_str)
                            element_dict['expression'] = exp_result

                        if str_file == 'substrates':
                            data = pd.read_csv(path)
                            sub_json = data.to_json(orient='records', force_ascii=False)
                            sub_str = sub_json.replace('[', '').replace(']', '').replace('\\', '').replace('null','None').replace('\u03bc', 'μ').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                            sub_result = eval(sub_str)
                            element_dict['substrates'] = sub_result

                        if str_file == 'inhibitors':
                            data = pd.read_csv(path)
                            inh_json = data.to_json(orient='records', force_ascii=False)
                            inh_str = inh_json.replace('[', '').replace(']', '').replace('\u03bc', 'μ').replace('null','None').replace('\\', '').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                            inh_result = eval(inh_str)
                            element_dict['inhibitors'] = inh_result

                        if str_file == 'ddi':
                            data = pd.read_csv(path)
                            # print(data.columns)  # 打印表头
                            # print(path)

                            # 替换列名
                            data.columns = ['DDI', 'Implicated Transporter', 'Interacting Drug', 'Affected Drug', 'AUC',
                                            'Cmax', 'CLR', 'CL/F', 't1/2', 'Effect on PD', 'Reference', 'More Details',
                                            'Interacting_Drug_link', 'Affected_Drug_link', 'Reference_link', 'DDI_link']
                            # data.name.isin([筛选元素])（name为列名）进行筛选，加负号的原因是想删除符合条件的行，不写负号是筛选出符合条件的行
                            # new_data = data[-data.AUC.isin(['Clinical PK Impact(fold change)'])]

                            # 将csv文件转换为json格式，使用to_json()，返回字符串
                            ddi_json = data.to_json(orient='records', force_ascii=False)

                            # 去掉开头和结尾处的
                            ddi_str = ddi_json.replace('[', '').replace(']', '').replace('\\', '').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')  # 可写成正则表达式

                            # 字符串转字典：用eval转换,并替换反斜杠
                            ddi_result = eval(ddi_str)

                            # 生成嵌套字典
                            element_dict['ddi'] = ddi_result

            drug_dict[dir_name] = element_dict
            # print(drug_dict)
            # 格式化输出字典,indent设置为4,输出真正的中文需要指定ensure_ascii=False
            # with open('/home/cqfnenu/nosql-biosets-master/transporter/transporters_json/' + dir_name + '.json', 'w') as f:
            with open('/home/cqfnenu/nosql-biosets-master/transporter/compounds_json/' + dir_name + '.json', 'w') as f:
                f.write(json.dumps(drug_dict, ensure_ascii=False, indent=6))


if __name__ == '__main__':
    main()

