"""
purpose: 公式计算自提点与中心点的距离（km）
author: QF.Chen
date: 2020/7/21
"""

from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import xlwt

def geodistance(lng1, lat1, lng2, lat2):

    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
    dlon = lng2-lng1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance = 2*asin(sqrt(a))*6371*1000   # 地球平均半径，6371km
    distance = round(distance/1000, 3)
    return distance

def main():

    path_1 = 'C:\\Users\\KerryChen\\Desktop\\距离计算_中心点.xlsx'
    df_1 = pd.read_excel(path_1)
    lng_1, lat_1 = df_1.shape

    print(lng_1, lat_1, type(df_1))
    # print(df_1)

    x = np.zeros((lng_1, lat_1-2))

    for i in range(0, lng_1):
        for j in range(2, lat_1):
            x[i][j-2] = df_1.ix[i, j]
    # print(x)


    dis_list = []
    # k = 0
    for i in range(lng_1):
        # dis = geodistance(x[i][0], x[i][1], 118.473126, 32.148817)
        dis = geodistance(x[i][0], x[i][1], 118.779852, 32.031915)
        # k = k + 1
        print(dis)
        dis_list.append(dis)

    return dis_list

def save_file(lis, file):
    # 将数据写入新文件
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    # 将数据写入第 i 行，第 j 列
    for i in range(15):
        sheet1.write(i, 0, lis[i])

    f.save(file)  # 保存文件
    print("xls格式表格写入数据成功！")


if __name__ == '__main__':
    path = 'C:\\Users\\KerryChen\\Desktop\\中心点_distance.xlsx'
    lis = main()
    save_file(lis, path)







