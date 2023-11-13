from src.kib_scrapper import LocalCatalogItems, KibCatalog
from selenium import webdriver
import json
import time
import numpy as np
import pandas as pd
import pickle
import os

def parser():
    with open('./config.json', 'r') as fo:
        conf = json.loads(fo.read())
    adresses = []
    with open('kib_addres.csv', 'r') as file:
        for line in file.readlines():
            line = line.rstrip()
            adresses.append(('Владимирская область', 'Владимир', line))
    print(adresses)
    kib_login = conf['kib_login']
    kib_password = conf['kib_password']
    data_folder = './parsed_data'

    driver = webdriver.Edge()
    catalog = KibCatalog(driver, kib_login=kib_login, kib_password=kib_password, save_path=data_folder)
    for ad in adresses:
        items = catalog.parse_catalog(*ad)
        df = items.get_dataframe()
        df.to_csv(ad[2]+'.csv')

def stolb_kb():
    zxc = os.listdir('C:\\Users\\Danila\\PycharmProjects\\kib_scrapper-main\\all')
    for i in zxc:
        df = pd.read_csv('C:\\Users\\Danila\\PycharmProjects\\kib_scrapper-main\\all\\'+i)
        df['name_shop'] = 'КБ'
        df.to_csv('C:\\Users\\Danila\\PycharmProjects\\kib_scrapper-main\\all_new\\'+i)

import requests


def get_bd_1():
    df = pd.read_csv('ул. Университетская, 8-а.csv')
    bd_info = pd.DataFrame()
    name = []
    category=[]
    info = []
    image = []
    price = []
    count = 0
    for index, row in df.iterrows():
        name.append(char_delete(row['name'].split('\n')[0]))
        info.append(row['name'].split('\n')[1])
        image.append(name[-1]+'.png')
        resource = requests.get(row['pic_url'])
        try:
            out = open("C:\\Users\\Danila\\PycharmProjects\\kib_scrapper-main\\img\\"+image[-1], 'wb')
            out.write(resource.content)
            out.close()
        except:
            print(name[-1])
            pass
        # convertImage("C:\\Users\\Danila\\PycharmProjects\\kib_scrapper-main\\img\\"+image[-1])
    bd_info['name'] = name
    bd_info['info'] = info
    bd_info['image'] = image
    bd_info.to_csv("C:\\Users\\Danila\\PycharmProjects\\kib_scrapper-main\\bd\\bg_kb_info.csv")


def char_delete(string):
    return ''.join(e for e in string if e.isalnum())


from PIL import Image


def convertImage(img_old):
    img = Image.open(img_old)
    img = img.convert("RGBA")

    datas = img.getdata()

    newData = []

    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(img_old, "PNG")
    print("Successful")


get_bd_1()