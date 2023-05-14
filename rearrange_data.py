# -*- coding: utf-8 -*-
#%%
import re
import os
import json
import pandas as pd

raw_data_path = './raw_data'
processed_data_path = './data'

song_info_path = 'song-warpper.txt'
song_coordinate_path = 'song-coordinate.txt'

origin_data_path = 'Data_1991_2022.xlsx'
arranged_data_path = 'data_13_22.csv'

coordinates = []

#%% 读取从网页复制的.txt文件，解析其中坐标并保存
'''
with open(os.path.join(raw_data_path, song_info_path), 'r', encoding='utf-8') as f:
    song_txt_ls = f.readlines()[0].split('</g>') # 2011 points in total
    for song in song_txt_ls[:-1]:
        song = song.split('>')[0]
        coordinate_ls = re.findall('\(.+\)', song)[0].strip('(').strip(')').split(',')
        coordinate_tup = tuple([float(x) for x in coordinate_ls])
        coordinates.append(coordinate_tup)
f.close()

with open(os.path.join(processed_data_path, song_coordinate_path), 'w', encoding='utf-8') as f:
    f.writelines([str(x) + '\n' for x in coordinates])
f.close()
'''

#%% 整合所有年份电影数据到一个.csv文件中（不含票房等统计数据）
base_df = pd.read_excel(os.path.join(raw_data_path, origin_data_path), sheet_name='2013').iloc[:-2]
base_df = base_df.drop(labels=range(base_df.shape[0]))
base_df = base_df.drop(labels='Release', axis=1) # 删去具体发布时间列，仅留下发布年份
base_df = base_df.drop(labels='Rank', axis=1)
for sheet_name in range(2013, 2023):
    df_tmp = pd.read_excel(os.path.join(raw_data_path, origin_data_path), sheet_name=str(sheet_name)).iloc[:-2]
    df_tmp = df_tmp.dropna()
    df_tmp['rank'] = [i + 1 for i in range(df_tmp.shape[0])]
    df_tmp['releaseYear'] = [sheet_name] * df_tmp.shape[0]
    df_tmp = df_tmp.drop(labels='Release', axis=1) # 删去具体发布时间列，仅留下发布年份
    df_tmp = df_tmp.drop(labels='Rank', axis=1)
    df_tmp = df_tmp.iloc[:201] # 每年仅取前201个电影
    base_df = pd.concat([base_df, df_tmp], ignore_index = True)
    print(sheet_name, df_tmp.shape[0])

print(base_df.shape[0])
#%%
base_df.dropna().to_csv(os.path.join(processed_data_path, arranged_data_path), index=False, encoding='utf-8')
# base_df.to_csv(os.path.join(processed_data_path, arranged_data_path), index=False)

