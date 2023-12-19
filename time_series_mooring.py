#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 07:26:56 2023

@author: JiM
looking at the Cape Cod Bay mooring
"""
import pandas as pd
from netCDF4 import Dataset
import datetime
from matplotlib import pylab as plt
import numpy as np
from conversions import c2f,distance

#get mooring data
df=Dataset('https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/221p1_rt.nc?waveTime[0:1:25041],waveHs[0:1:25041],sstTime[0:1:149326],sstSeaSurfaceTemperature[0:1:149326]')
time = df.variables['sstTime'][:].data
dtime=[]
for k in range(len(time)):
    dtime.append(datetime.datetime.fromtimestamp(time[k]))
sst  = list(c2f(df.variables['sstSeaSurfaceTemperature'][:].data)[0])

#get miniboat data
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Rock_Star_4s.csv')
x=df['longitude'].values
y=df['latitude'].values
t=list(df['water_temp'].values)
# find closest approach to morring and convert time
cla=41.84
clo=-70.32
dt,dist=[],[]
for j in range(len(df)):
    dt.append(pd.to_datetime(df['moment_date'][j]))
    dist.append(distance((y[j],x[j]),(cla,clo))[0])
ind=np.argmin(dist)    



fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.plot(dt,t,color='r',linewidth=3,label='miniboat Rock Star')
ax.plot(dtime,sst,color='b',linewidth=3,label='mooring CDIP221')
ax.text(dt[ind],t[ind],'closest')
ax.set_ylabel('fahrenheit',fontsize=16)
ax.set_ylim(np.nanmin(t),np.nanmax(t))
ax.set_xlim(np.nanmin(dt),np.nanmax(dt))
ax.legend()