#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   set_coordinate_by_packcircles.py
@Time    :   2023/05/14 21:10:33
@Author  :   Lin Junwei
@Version :   1.0
@Desc    :   None
'''

#%%
import packcircles as pc
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
radii =  [28,12,51,26,10,16,24,25,59,11,29,40,16,11,10,26,39,16,48,36,28]
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
ax.set(xlim=(-150, 140), ylim=(-180, 170))
plt.axis('off')
plt.show()
#%%