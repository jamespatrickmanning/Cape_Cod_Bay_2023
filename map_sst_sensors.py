#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 06:39:08 2023

@author: JiM
"""
import pandas as pd
import numpy as np
from matplotlib import pylab as plt
from conversions import c2f
import os,imageio
import conda
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
#os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
#os.environ['PROJ_LIB'] = 'C:\\Users\\james.manning\\Anaconda3\\pkgs\\proj-7.1.0-h7d85306_1\\Library\share'
os.environ['PROJ_LIB'] = '/home/user/anaconda3/pkgs/proj-8.2.1-h277dcde_0/share'
#conda install -c conda-forge basemap (to get basemap on my Linux machine in Nov 2022)

from mpl_toolkits.basemap import Basemap
def getgbox(area):
  # gets geographic box based on area
  if area=='SNE':
    gbox=[-71.,-67.,39.5,42.] # for SNE shelf east
  elif area=='SNW':
    gbox=[-71.5,-69.5,40.,41.75] # for SNw shelf west
  elif area=='MABN':
    gbox=[-73.,-68.,39.,42.] # for SNw shelf west  
  elif area=='OOI':
    gbox=[-71.5,-69.,39.5,41.6] # for OOI
  elif area=='GBANK':
    gbox=[-71.,-66.,40.,42.] # for GBANK
  elif area=='GBANK_RING':
    gbox=[-71.,-65.,39.,42.5] # for typical GBANK Ring 
  elif area=='GS':           
    gbox=[-71.,-63.,38.,42.5] # for Gulf Stream
  elif area=='NorthShore':
    gbox=[-71.,-69.5,41.75,43.25] # for north shore
  elif area=='Gloucester':
    gbox=[-71.,-70.,42.25,43.] # for north shore
  elif area=='IpswichBay':
    gbox=[-71.,-70.,42.5,43.] # for IpswitchBay
  elif area=='CCBAY':
    gbox=[-70.75,-69.8,41.5,42.23] # CCBAY
  elif area=='inside_CCBAY':
    gbox=[-70.75,-70.,41.7,42.15] # inside CCBAY
  elif area=='NEC':
    gbox=[-68.,-63.,38.,43.5] # NE Channel
  elif area=='NE':
    gbox=[-76.,-66.,35.,44.5] # NE Shelf 
  return gbox

area='inside_CCBAY'
gb=getgbox(area)
fig = plt.figure()

df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Riptide_8s.csv')
x2=df['longitude'].values
y2=df['latitude'].values
t2=df['water_temp'].values
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Rock_Star_3s.csv')
x3=df['longitude'].values
y3=df['latitude'].values
t3=df['water_temp'].values
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Riptide_9s.csv')
x4=df['longitude'].values
y4=df['latitude'].values
t4=df['water_temp'].values
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Rock_Star_4s.csv')
x5=df['longitude'].values
y5=df['latitude'].values
t5=df['water_temp'].values
#m = Basemap(projection='stere',lon_0=(gb[0]+gb[1])/2.,lat_0=(gb[2]+gb[3])/2.,lat_ts=0,llcrnrlat=gb[2],urcrnrlat=gb[3],\
#llcrnrlon=gb[0],urcrnrlon=gb[1],rsphere=6371200.,resolution='c',area_thresh=100)# JiM changed resolution to "c" for crude
m = Basemap(projection='stere',lon_0=np.mean(x5),lat_0=np.mean(y5),lat_ts=0,llcrnrlat=np.min(y5)-.1,urcrnrlat=np.max(y5)+.1,\
llcrnrlon=np.min(x5)-.1,urcrnrlon=np.max(x5)+.1,rsphere=6371200.,resolution='f',area_thresh=100)# JiM changed resolution to "c" for crude
# draw coastlines, state and country boundaries, edge of map.
m.drawcoastlines()
m.fillcontinents(color='gray',zorder=3)

# draw parallels.
if (area=='IpswichBay') or (area=='Gloucester'):
    labint=0.2
    dept_clevs=[30,50,100, 150]
elif area[0:3]=='CCB':
    labint=0.5
    dept_clevs=[30,50,100]
elif (area=='NE') or (area=='SNW'):
    labint=1.0
    dept_clevs=[50,100,1000]
    x,y=m(-69.5,40.5)    
    #plt.text(x,y,'Great South Channel',fontsize=12, rotation=0) 

elif (area=='NorthShore'):
    labint=.50
    dept_clevs=[50,100,150]  
elif (area=='GBANK') or (area=='GBANK_RING'):
    labint=1.0
    dept_clevs=[50,100,150]
    x,y=m(-68.3,40.65)    
    plt.text(x,y,' Georges Bank',fontsize=16, rotation=30) 
else:
    labint=.1
    dept_clevs=[30,50,100, 150,300,1000]
parallels = np.arange(0.,90,labint)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=12)
# draw meridians
meridians = np.arange(180.,360.,labint)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=12)
df=pd.read_csv('/home/user/drift/data/EPMBD_084_1.csv')
x=df['LON'].values
y=df['LAT'].values
t1=c2f(df['buoy_temp_F'].values)[0]
mx1,my1=m(x,y)
mx2,my2=m(x2,y2)
mx3,my3=m(x3,y3)
mx4,my4=m(x4,y4)
mx5,my5=m(x5,y5)
plot = plt.scatter(mx1, my1, s= 10, c = t1, cmap='coolwarm')
plot = plt.scatter(mx2, my2, s= 10, c = t2, cmap='coolwarm')
plot = plt.scatter(mx3, my3, s= 10, c = t3, cmap='coolwarm')
plot = plt.scatter(mx4, my4, s= 10, c = t4, cmap='coolwarm')
plot = plt.scatter(mx5, my5, s= 10, c = t5, cmap='coolwarm')
fig.colorbar(plot)
#plt.grid(True, 'both')

# add another scatterplot
'''
x_line = np.linspace(np.min(x), np.max(x), num=1000)
y_line = x_line + np.sin(np.pi * x_line)
z_line = 5 * x_line
plt.scatter(x_line, y_line, c=z_line, s=0.1, cmap='coolwarm')
'''

plt.show()
plt.savefig('SST_MakeBuoy_Miniboats.png')