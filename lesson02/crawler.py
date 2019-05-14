# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests
import os
import urllib
from lxml import html
path_ls8 = '/home/psdz/landsat8_cca'


def mkdir(path):
    flag = os.path.exists(path)
    if not flag:
        # os.mkdir(path)
        os.makedirs(path)


def cbk(a, b, c):
    '''
    
    :param a: 已下截
    :param b: 数据块的大小 
    :param c: 远程文件的大小
    :return: 
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' %per

ls8_target = 'https://landsat.usgs.gov/landsat-8-cloud-cover-assessment-validation-data'
ls8_req = requests.get(url=ls8_target)
ls8_txt = ls8_req.text
ls8_bf = bs(ls8_txt)
tar_adds = ls8_bf.find_all('td', class_='column2 rtecenter')
for i in range(len(tar_adds)):
    print tar_adds[i]
print len(tar_adds)
temp_tiff_num = []
a_bf = bs(str(tar_adds))
a_bf = a_bf.find_all('a')
download_add = [] # 下载地址
for each in a_bf:
    download_add.append(each.get('href'))
    temp_tiff_num.append(each.string)
    # print each.get('href'), ' ', each.string
print download_add, '\n', temp_tiff_num

scenes = ls8_bf.find_all('td', class_='column1 rtecenter')
scenes = bs(str(scenes))
scenes = scenes.find_all('strong')
temp_scenes_name = []
for name in scenes:
    # print name
    temp_scenes_name.append(name.string)
# for str_name in scenes_name:
#     str_name.replace('u', '_')
# print scenes_name
# print scenes, scenes.string
scenes_names = []
for name in temp_scenes_name:
# 此处有坑，需要解码编码
    name = name.encode('unicode-escape').decode('string_escape')
    if name=='Grass/Crops':
        name = 'Grass_Crops'
    elif name == 'Snow/Ice':
        name = 'Snow_Ice'
    scenes_names.append(name)
print scenes_names
tiff_num = []
for tiff in temp_tiff_num:
    tiff = tiff.encode('unicode-escape').decode('string_escape')
    # print name
    tiff_num.append(tiff)
print tiff_num
scenes_path = []
mkdir(path_ls8)
for folder in scenes_names:
    temp_path = path_ls8 + '/' + folder
    scenes_path.append(temp_path)
    mkdir(temp_path)
j = 0
for i in range(len(download_add)):
    temp_path = scenes_path[i/12]+'/'+tiff_num[i]+'.tar.gz'
    if os.path.exists(temp_path): 
        print 'exist'
        continue
    urllib.urlretrieve(download_add[i], temp_path, cbk)
        #print scenes_path[i/12]+'/'+tiff_num[i]
    print temp_path, i/12
    print download_add[i]
print len(download_add)


