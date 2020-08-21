#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/8/13 09:32
# @Author  : Qiufen.chen
# @Email   : 1760812842@qq.com
# @File    : parse_csv.py
# @Software: PyCharm
# @purpose : Python converts .CSV files into.JSON format files
'''

import pandas as pd
import json
import os
import importlib, sys
importlib.reload(sys)


def main():

    # dir_path = '/home/cqfnenu/nosql-biosets-master/transporter/transporters_data/'
    dir_path = '/home/cqfnenu/nosql-biosets-master/transporter/compounds_data'

    # Traverse the document
    for (root_1, dirs_1, files_1) in os.walk(dir_path):
        for dir_name in dirs_1:

            # Create a dictionary of Trasporter
            # element_dict = {'transporter_name': dir_name }

            # Create a dictionary of Compound
            element_dict = {'compound_name': dir_name}

            for (root_2, dirs_2, files_2) in os.walk(os.path.join(root_1, dir_name)):
                for file_name in files_2:
                    str_file = str(file_name.split('.')[0])
                    path = os.path.join(root_2, file_name)

                    if os.path.isfile(path):

                        if str_file == 'basic_information':
                            data = pd.read_csv(path)
                            info_json = data.to_json(orient='records', force_ascii=False)
                            info_str = info_json.replace('[', '').replace(']', '').replace('\\', '').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')
                            info_result = eval(info_str)
                            element_dict['basic_information'] = info_result

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
                            # print(data.columns)  # Print the header
                            # print(path)

                            # Replace the header name
                            data.columns = ['DDI', 'Implicated Transporter', 'Interacting Drug', 'Affected Drug', 'AUC',
                                            'Cmax', 'CLR', 'CL/F', 't1/2', 'Effect on PD', 'Reference', 'More Details',
                                            'Interacting_Drug_link', 'Affected_Drug_link', 'Reference_link', 'DDI_link']

                            # Converts the CSV file to JSON format, using to_json(), and returns a string
                            ddi_json = data.to_json(orient='records', force_ascii=False)

                            # Remove the beginning of '[' and end of ']'
                            ddi_str = ddi_json.replace('[', '').replace(']', '').replace('\\', '').replace('../', 'http://transportal.compbio.ucsf.edu/compounds/')  # 可写成正则表达式

                            # String to dictionary: Convert with eval()
                            ddi_result = eval(ddi_str)

                            # Generate nested dictionaries
                            element_dict['drug_drug_interaction'] = ddi_result

            # drug_dict[dir_name] = element_dict
            # print(drug_dict)

            # Format the output dictionary,indent set to 4, and specify ensure_ASCII =False to output real Chinese
            # with open('/home/cqfnenu/nosql-biosets-master/transporter/transporters_json/' + dir_name + '.json', 'w') as f:
            with open('/home/cqfnenu/nosql-biosets-master/transporter/compounds_json/' + dir_name + '.json', 'w') as f:
                f.write(json.dumps(element_dict, ensure_ascii=False, indent=6))


if __name__ == '__main__':
    main()

