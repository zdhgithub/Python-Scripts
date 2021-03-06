#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 11:24:15 2016

use main()
@author: 老徐
"""
import argparse
from datetime import datetime
from datetime import timedelta
from pandas import read_excel
from numpy import array
from numpy import nan


parser = argparse.ArgumentParser(description='为小胖写的自动计算出勤时间的小程序')
parser.add_argument('-f', '--file-path', action='store', dest='filename', help='文件路径')
parser.add_argument('-s', '--sheet-name', action='store', dest='sheetname', default='17.18.19', help='表名，默认为"17.18.19"')
parser.add_argument('-c', '--column-number', action='store', dest='column', default='3', help='第几栏，默认为"3"')

def str2time(str):
    try:
        return datetime.strptime(str, '%H:%M')
    except:
        #print('err with time as', str)
        return datetime.strptime('0', '%H')


def main():
    args = parser.parse_args()
    if not args.filename:
        print('没有输入文件路径，请使用 -h 参数查看帮助')
        exit(1)
    filename = args.filename
    sheetname = args.sheetname
    column = args.column
    xls_column = {'1':'A:N', '2':'P:AC', '3':'AE:AR'}
    info_column = {'1': 'B,J', '2': 'Q,Y', '3': 'AF,AN'}
    try:
        data = read_excel(filename, sheetname=sheetname, parse_cols=xls_column[column], skiprows=10)
    except:
        sheetname = 0
    data = read_excel(filename, sheetname=sheetname, parse_cols=xls_column[column], skiprows=10)
    info = read_excel(filename, sheetname=sheetname, parse_cols=info_column[column]).ix[:1, :].values
    print('  姓名  ： %s\n记录时间： %s' % (info[0, 1], info[1, 0]))
    data = data.replace(to_replace={'旷工' : nan})
    data = array(data)
    data = data[:,[1,3,6,8,10,12]]
    time_of_a_day = timedelta(0)
    for _ in range(len(data)):
        for __ in range(3):
            if (data[_, __*2] is not nan) and (data[_, __*2+1] is not nan):
                time_of_a_day += str2time(data[_, __*2+1]) - str2time(data[_, __*2])
    result = time_of_a_day
    sec = result.total_seconds()
    s = sec % 3600
    hour = int((sec - s) / 3600)
    minutes = s / 60
    print('出勤时间： {0:d}小时{1:.0f}分钟'.format(hour, minutes))
    print('for my lover, 小胖儿～, 13自动化老徐')
    return result


if __name__ == "__main__":
    main()
