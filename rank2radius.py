#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   rank2radius.py
@Time    :   2023/05/15 21:29:12
@Author  :   Lin Junwei
@Version :   1.0
@Desc    :   None
'''
#%%
import pandas as pd 
import numpy as np 
import packcircles as pc
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

#%%


def rank2radius(rk):
    ''' rank => radius '''
    if rk >= 1 and rk <= 5:
        rd = 25
    elif rk >= 5 and rk <= 10:
        rd = 22
    elif rk >= 11 and rk <= 30:
        rd = 20
    elif rk >= 31 and rk <= 50:
        rd = 17
    elif rk >= 51 and rk <= 70:
        rd = 15
    elif rk >= 71 and rk <= 90:
        rd = 13
    elif rk >= 91 and rk <= 110:
        rd = 9
    elif rk >= 111 and rk <= 130:
        rd = 7
    elif rk >= 131 and rk <= 170:
        rd = 5
    elif rk >= 171 and rk <= 201:
        rd = 3
    else: # 年份坐标
        rd = 50
    return rd

year_coordinates = {
2013: (-222.07792207792207, 250.0),
2014: (24.675324675324678, 250.0),
2015: (271.4285714285714, 250.0),
2016: (518.1818181818181, 250.0),
2017: (764.9350649350649, 250.0),
2018: (1011.6883116883116, 250.0),
2019: (1258.4415584415585, 250.0),
2020: (1505.1948051948052, 250.0),
2021: (1751.948051948052, 250.0),
2022: (1998.7012987012988, 250.0),
}
#%%

def year2circle(year, df):
    '''year to circle coordinate'''
    # year = 2013
    df_coordinates = df[df['releaseYear'] == year].copy()

    df_coordinates = df_coordinates.sample(frac=1)
    df_year_circle = pd.DataFrame(data = [[np.nan] * 7], columns=df_coordinates.columns)
    df_coordinates = df_year_circle.append(df_coordinates).reset_index(drop=True)
    df_coordinates['radius'] = df_coordinates['rank'].apply(lambda x: rank2radius(x))

    rk_ls = df_coordinates['radius'].tolist()
    radius_ls = [rank2radius(rk) for rk in rk_ls]

    circles = pc.pack(radius_ls)
    x_ls = []
    y_ls = []

    for (x, y, radius) in circles:
        x_ls.append(x)
        y_ls.append(y)

    
    df_coordinates['x'] = x_ls
    df_coordinates['y'] = y_ls

    return df_coordinates




#%% 
df  = pd.read_csv('./data/data_13_22.csv', sep=';', encoding='gbk')
df1 = year2circle(2013, df=df)
df1.to_csv('./data/data_13.csv', index=False)
# %%
radii =  df1['radius'].tolist()
fig, ax = plt.subplots()
cmap = get_cmap('coolwarm_r')
circles = pc.pack(radii)
for (x,y,radius) in circles:
    patch = plt.Circle(
        (x,y),
        radius,
        color=cmap(radius/max(radii)),
        alpha=0.65
    )
    ax.add_patch(patch)
fig.set_figheight(15)
fig.set_figwidth(15)
ax.set(xlim=(-500, 500), ylim=(-500, 500))
plt.axis('off')
plt.show()


# %%
