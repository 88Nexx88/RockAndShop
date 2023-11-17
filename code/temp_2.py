import pandas as pd
import os

df = pd.read_csv('/home/valery/Desktop/IAS/RockAndShop/code/Shops/KB/мкр Юрьевец,ул. Всесвятская, 3.csv', usecols=['name', 'price', 'pic_url', 'address', 'name_shop'])
csv_folder = '/home/valery/Desktop/IAS/RockAndShop/code/Shops/KB/'
print(len(set(df['name'].tolist())))

csvs = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
print(csvs)