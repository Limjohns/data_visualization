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
arranged_data_path = 'data.csv'

coordinates = []

#%% 读取从网页复制的.txt文件，解析其中坐标并保存
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

#%% 整合所有年份电影数据到一个.csv文件中（不含票房等统计数据）
base_df = pd.read_excel(os.path.join(raw_data_path, origin_data_path), sheet_name=0).iloc[:-2]
for sheet_name in range(1991, 2023):
    df_tmp = pd.read_excel(os.path.join(raw_data_path, origin_data_path), sheet_name=str(sheet_name)).iloc[:-2]
    df_tmp = df_tmp.dropna()
    df_tmp['Rank'] = [i + 1 for i in range(df_tmp.shape[0])]
    base_df = pd.concat([base_df, df_tmp], ignore_index = True)
#%%
base_df.dropna().to_csv(os.path.join(processed_data_path, arranged_data_path), index=False)
# base_df.to_csv(os.path.join(processed_data_path, arranged_data_path), index=False)



# %%
