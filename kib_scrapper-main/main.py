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

stolb_kb()