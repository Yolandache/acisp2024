# -*- coding: utf-8 -*-
# @Time    : 2023/4/15 20:40
# @Author  : Jin Au-yeung
# @File    : normaldownload.py
# @Software: PyCharm
import glob
import multiprocessing

import config
from Spider import Spider
import os
from GetAppCsv import ReadCsv
import pandas as pd
from multiprocessing import Pool

def process_apks(apk):
    # 创建一个 Spider 对象
    spider = Spider()

    app_info = spider.download(apk)
    if app_info is None:
        return None
    with open('normal_apps.txt', 'a') as f:
        f.write(apk['download_url']+'\n')


def getAnalysis():
    category_list = ['APPLICATION', 'ANDROID_WEAR', 'ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY',
                     'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'EDUCATION',
                     'ENTERTAINMENT', 'EVENTS', 'FINANCE', 'FOOD_AND_DRINK', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME',
                     'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'MAPS_AND_NAVIGATION', 'MEDICAL', 'MUSIC_AND_AUDIO',
                     'NEWS_AND_MAGAZINES', 'PARENTING', 'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'SHOPPING',
                     'SOCIAL', 'SPORTS', 'TOOLS', 'TRAVEL_AND_LOCAL', 'VIDEO_PLAYERS', 'WATCH_FACE', 'WEATHER',
                     'FAMILY']
    print(f'共计: {len(category_list)} 个类别')
    status_path_list = [os.path.join(config.DATA_PATH, 'status', path + '_apps_status.txt') for path in category_list]
    # print(status_path_list)
    # 存储应用状态的字典

    # 逐个读取应用状态文件，将内容存入字典中
    app_status = {}
    for status_file in status_path_list:
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                # 读取文件内容并将其按逗号分隔
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split(',')
                    app_status[line[0]] = line[1]

    return app_status
import random
def main():
    csv_path = r'D:\secComm\utils\apps.csv'
    # 假设您有一个包含所有应用信息的列表
    apps = ReadCsv(csv_path)
    with open('normal_apps.txt','r',encoding='utf-8') as fp:
        normal_apps = fp.readlines()
        normal_apps = [app.strip() for app in normal_apps]
    normal_apps = list(set(normal_apps))
    print(len(normal_apps))
    print(normal_apps[0])
    print(apps[0])
    # 从apps中提取所有的download_url字段，并将它们存储在一个列表中
    download_urls = [app['download_url'] for app in apps]
    # 遍历normal_apps列表中的每个元素，如果该元素在download_url列表中，则将该元素从download_url列表中删除
    for url in normal_apps:
        if url in download_urls:
            download_urls.remove(url)
    # 使用列表推导式，遍历apps中的每个字典，并根据download_url字段判断该字典是否应该保留
    new_apps = [app for app in apps if app['download_url'] not in normal_apps]
    print(len(new_apps))
    print(new_apps[0])

    # 设置进程数量
    num_processes = 16
    # 使用 multiprocessing.Pool 实现多进程并行处理
    with Pool(processes=num_processes) as pool:
        pool.map(process_apks, new_apps)


if __name__ == "__main__":
    main()

