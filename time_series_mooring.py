#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 07:26:56 2023

@author: JiM
looking at the Cape Cod Bay Dec 2023 observations and model
"""
import pandas as pd
from netCDF4 import Dataset
import datetime
from matplotlib import pylab as plt
import numpy as np
from conversions import c2f,distance,sd2uv,ll2uv_datetime


#get CDIP mooring data 
cla=41.84
clo=-70.32
# FIRST at CDIP221 get SST
df=Dataset('https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/221p1_rt.nc?waveTime[0:1:25484],waveHs[0:1:25484],sstTime[0:1:151975],sstSeaSurfaceTemperature[0:1:151975]')
time = df.variables['sstTime'][:].data
whtime=df.variables['waveTime'][:].data
dtime=[]
for k in range(len(time)):
    dtime.append(datetime.datetime.fromtimestamp(time[k]))
dtimewh,dtwh=[],[]
for k in range(len(whtime)):
    dtimewh.append(datetime.datetime.fromtimestamp(whtime[k]))
    dtwh.append(datetime.datetime.fromtimestamp(whtime[k]))
sst  = list(c2f(df.variables['sstSeaSurfaceTemperature'][:].data)[0])
wh= df.variables['waveHs'][:].data
# now get current spd and dir
'''
url='https://erddap.cdip.ucsd.edu/erddap/tabledap/acm_agg.csvp?station_id%2Ctime%2CacmSpeed%2CacmDirection&time%3E=2023-12-15T00%3A17%3A12Z&time%3C=2023-12-17T00%3A17%3A12Z&acmFlagPrimary=1&orderByMax(%22station_id%2Ctime%22)'
df=pd.read_csv(url)
df=df[df['station_id']==221]
dtc=df['time (UTC)']
dspd=df['acmSpeed (meter/second)']*100.
ddir=df['acmDirection (degreeT)']
'''
df=pd.read_csv('44090.adcp.txt',skiprows=2,sep='\s+') # after downloading from https://www.ndbc.noaa.gov/data/realtime2/44090.adcp
df=df.iloc[::-1]
dtc=[]
for k in range(len(df)):
    dtc.append(datetime.datetime(df['2023'][k],df['12'][k],df['25'][k],df['22'][k],df['00'][k]))
dspd=df['3'].values
ddir=df['40'].values
[u,v]=sd2uv(dspd,ddir)

# Now from NDBC mooring 44018
df=pd.read_csv('https://www.ndbc.noaa.gov/data/realtime2/44018.txt',skiprows=range(1,1),sep='\s+') # after downloading from https://www.ndbc.noaa.gov/data/realtime2/44090.adcp
df=df[1:] # gets rid of units line
df=df.iloc[::-1]
df=df[df['WSPD']!='MM']
df=df[df['WDIR']!='MM']
dtw,dspdw,ddirw=[],[],[]
for k in range(len(df)):
    dtw.append(datetime.datetime(int(df['#YY'].values[k]),int(df['MM'].values[k]),int(df['DD'].values[k]),int(df['hh'].values[k]),int(df['mm'].values[k])))
    dspdw.append(df['WSPD'].astype(float).values[k]*10)
    ddirw.append(df['WDIR'].astype(float).values[k])
    [uw,vw]=sd2uv(dspdw,ddirw)


#get miniboat data Rockstar_3
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Rock_Star_3s.csv')
xr3=df['longitude'].values
yr3=df['latitude'].values
tr3=list(df['water_temp'].values)
pitchr3=list(df['max_pitch'].values)
# find closest approach to morring and convert time
dtr3,dist=[],[]
for j in range(len(df)):
    dtr3.append(pd.to_datetime(df['moment_date'][j]))
    dist.append(distance((yr3[j],xr3[j]),(cla,clo))[0])
indr3=np.argmin(dist)
#derive u & v from time.lat,lon
[umbr3,vmbr3,smbr3,ddtmbr3]=ll2uv_datetime(dtr3,yr3,xr3)    

#get miniboat data Rockstar_3
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Rock_Star_4s.csv')
xr4=df['longitude'].values
yr4=df['latitude'].values
tr4=list(df['water_temp'].values)
pitchr4=list(df['max_pitch'].values)
# find closest approach to morring and convert time
dtr4,dist=[],[]
for j in range(len(df)):
    dtr4.append(pd.to_datetime(df['moment_date'][j]))
    dist.append(distance((yr4[j],xr4[j]),(cla,clo))[0])
indr4=np.argmin(dist)
#derive u & v from time.lat,lon
[umbr4,vmbr4,smbr4,ddtmbr4]=ll2uv_datetime(dtr4,yr4,xr4)

#get miniboat data Riptide_8
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Riptide_8s.csv')
xrt8=df['longitude'].values
yrt8=df['latitude'].values
trt8=list(df['water_temp'].values)
pitchrt8=list(df['max_pitch'].values)
# find closest approach to morring and convert time
dtrt8,dist=[],[]
for j in range(len(df)):
    dtrt8.append(pd.to_datetime(df['moment_date'][j]))
    dist.append(distance((yrt8[j],xrt8[j]),(cla,clo))[0])
indrt8=np.argmin(dist)
#derive u & v from time.lat,lon
[umbrt8,vmbrt8,smbrt8,ddtmbrt8]=ll2uv_datetime(dtrt8,yrt8,xrt8)    

#get miniboat data Riptide_9
df=pd.read_csv('https://educationalpassages.org/wp-content/uploads/csv/sensor/Riptide_9s.csv')
xrt9=df['longitude'].values
yrt9=df['latitude'].values
trt9=list(df['water_temp'].values)
pitchrt9=list(df['max_pitch'].values)
# find closest approach to morring and convert time
dtrt9,dist=[],[]
for j in range(len(df)):
    dtrt9.append(pd.to_datetime(df['moment_date'][j]))
    dist.append(distance((yrt9[j],xrt9[j]),(cla,clo))[0])
indrt9=np.argmin(dist)
#derive u & v from time.lat,lon
[umbrt9,vmbrt9,smbrt9,ddtmbrt9]=ll2uv_datetime(dtrt9,yrt9,xrt9)

#get makerbuoy data
df=pd.read_csv('/home/user/drift/data/EPMBD_084_1.csv')
#df2=pd.read_csv('/home/user/drift/data/EPMBD_085_1.csv')
#df=pd.concat([df1,df2],ignore_index=True)
dtmb=pd.to_datetime(df['time_stamp'])
pitchmb=list(df['max_pitch'].values)

#get SD drifter data
df=pd.read_csv('https://studentdrifters.org/tracks/drift_fhs_2023_2.csv')
df=df.drop('Unnamed: 0',axis=1)
df=df.drop_duplicates(ignore_index=True)
df=df[df['ID']==230410708]
xd=df['LAT'].values
yd=df['LON'].values
dtd,difft=[],[]
for j in range(len(df)):
    dtd.append(datetime.datetime(2023,df['MTH'].values[j],df['DAY'].values[j],df['HR_GMT'].values[j],df['MIN'].values[j]))
[ud,vd,sd,ddt]=ll2uv_datetime(dtd,yd,xd)
for k in range(len(dtd)-1):
    difft.append((dtd[k+1]-dtd[k]).total_seconds()/3600.) # hours between samples


# plot sst for Rockstar_3 as well as Riptide 8
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.plot(dtr3,tr3,color='r',linewidth=3,label='miniboat Rock Star_3')
ax.plot(dtrt8,trt8,color='c',linewidth=3,label='miniboat Riptide_8')
ax.plot(dtime,sst,color='b',linewidth=3,label='mooring CDIP221')
ax.text(dtr3[indr3],tr3[indr3]+(np.nanmax(tr3)-np.nanmin(tr3))/60,'closest difference  = '+'%s' % float('%.1g' % dist[indr3])+' km',verticalalignment='bottom',horizontalalignment='center')
ax.plot(dtr3[indr3],tr3[indr3],'o',markersize=10,color='k')
ax.set_ylabel('fahrenheit',fontsize=16)
ax.set_ylim(np.nanmin(tr3)-1,np.nanmax(tr3)+1)
ax.set_xlim(np.nanmin(dtr3),np.nanmax(dtr3))
ax.legend()
plt.savefig('SST_time_series_Rockstar_3.png')

# plot sst for Rockstar_ 4 as well as Riptide 9
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.plot(dtr4,tr4,color='r',linewidth=3,label='miniboat Rock Star_4')
ax.plot(dtrt9,trt9,color='c',linewidth=3,label='miniboat Riptide_9')
ax.plot(dtime,sst,color='b',linewidth=3,label='mooring CDIP221')
ax.text(dtr4[indr4],tr4[indr4]-(np.nanmax(tr4)-np.nanmin(tr4))/60,'closest difference  = '+'%s' % float('%.1g' % dist[indr4])+' km',verticalalignment='top',horizontalalignment='center')
ax.plot(dtr4[indr4],tr4[indr4],'o',markersize=10,color='k')
ax.set_ylabel('fahrenheit',fontsize=16)
ax.set_ylim(np.nanmin(tr4),np.nanmax(tr4))
ax.set_xlim(np.nanmin(dtr4),np.nanmax(dtr4))
ax.legend()
plt.savefig('SST_time_series_Rockstar_4.png')

#plot wave height, pitch, moored surface current, and wind during Rockstar_4
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.plot(dtr4,pitchr4,color='r',linewidth=3,label='miniboat Rockstar_4 pitch (angle)')
#ax.plot(dtmb,pitchmb,color='y',linewidth=3,label='MakerBuoy_84 pitch (angle)')
ax.plot(dtwh,wh*100,color='b',linewidth=3,label='mooring CDIP221 wave height (cm)')
ax.plot(dtr4[indr4],np.mean(wh),'o',markersize=10,color='k')
ax.plot(dtc[::-1],dspd[::-1],linewidth=3,color='c',label='mooring CDIP221 surface current speed (cm/s)')
ax.plot(ddtmbr4,smbr4,linewidth=3,color='m',label='minboat Rock Star speed (cm/s)')
ax.plot(dtw,dspdw,linewidth=3,color='g',label='mooring 44018 10xwind speed (m/s)')
ax.set_ylabel('sea state and surface current',fontsize=16)
#ax.set_ylim(np.nanmin(t),np.nanmax(t))
ax.set_ylim(0,200)
ax.set_xlim(np.nanmin(dtr4),np.nanmax(dtr4))
ax.legend()
plt.savefig('WH_time_series_Rockstar_4.png')

#plot wave height, pitch, moored surface current, and wind during Rockstar_3
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.plot(dtr3,pitchr3,color='r',linewidth=3,label='miniboat Rockstar_3 pitch (angle)')
ax.plot(dtmb,pitchmb,color='y',linewidth=3,label='MakerBuoy_84 pitch (angle)')
ax.plot(dtwh,wh*100,color='b',linewidth=3,label='mooring CDIP221 wave height (cm)')
ax.plot(dtr3[indr4],np.mean(wh),'o',markersize=10,color='k')
ax.plot(dtc[::-1],dspd[::-1],linewidth=3,color='c',label='mooring CDIP221 surface current speed (cm/s)')
ax.plot(ddtmbr3,smbr3,linewidth=3,color='m',label='minboat Rock Star_3 speed (cm/s)')
ax.plot(dtw,dspdw,linewidth=3,color='g',label='mooring 44018 10xwind speed (m/s)')
ax.set_ylabel('sea state and surface current',fontsize=16)
#ax.set_ylim(np.nanmin(t),np.nanmax(t))
ax.set_ylim(0,200)
ax.set_xlim(np.nanmin(dtmb),np.nanmax(dtmb))
ax.legend()
plt.savefig('WH_time_series_Rockstar_3.png')

#plot wind speed and miniboat speed with a breakdown of u & v
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.plot(dtc[::-1],dspd[::-1],linewidth=3,color='c',label='mooring CDIP221 surface current speed (cm/s)')
ax.plot(ddtmbr3,smbr3,linewidth=3,color='m',label='minboat Rock Star_3 speed (cm/s)')
ax.plot(dtw,dspdw,linewidth=3,color='g',label='mooring 44018 10xwind speed (m/s)')
ax.set_ylabel('wind speed * 10 (m/s) and miniboat speed (cm/s)',fontsize=16)
#ax.set_ylim(np.nanmin(t),np.nanmax(t))
ax.set_ylim(0,200)
ax.set_xlim(np.nanmin(dtr3),np.nanmax(dtr3))
ax.legend()
plt.savefig('wind_vs_miniboat_speed.png')

# plot mooring wave with sample time of drifter
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
#ax.plot(dtd,[1]*len(dtd),'.',markersize=4)
ax.plot(dtwh,wh*10,color='b',label='wave height (m) at mooring X 10')
ax.plot(ddt,difft,'.',markersize=5,color='r',label='hours between transmissions')
ax.set_xlim(np.nanmin(dtd),np.nanmax(dtd))
ax.legend()
ax.set_ylabel('sea state & hours',fontsize=16)
ax.set_title('loss of transmissions due to sea state')
plt.savefig('wh_vs_transmissions.png')

