# check glimb output

import pandas as pd
import numpy  as np 
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
import glob
import os
import platform

if platform.system()=='Darwin':
    hd = '/Users/ameghino/'
elif platform.system()=='Linux':
    hd = '/home/calving/'

def datenum2datetime(matlab_datenum):
    # MATLAB base date is 0000-01-01, while Python's datetime starts at 0001-01-01.
    # Offset is 366 days.
    python_base_date = datetime(1, 1, 1)
    offset = timedelta(days=366)
    
    # Convert MATLAB date number to Python datetime
    converted_date = python_base_date + timedelta(days=matlab_datenum) - offset
    return converted_date


# sum up discharge for all elevation and show time series.
path = hd + '/Nextcloud/fortran/glimb/output/'

mb200 = pd.read_csv(path + 'mb0210_obs_1996_2024.csv')
mb200['date'] = mb200.apply(lambda row: datetime(int(row['yr']), 1, 1) + timedelta(days=int(row['doy']) - 1), axis=1)
mb200.set_index('date', inplace=True)

monthly_sum = mb200['melt'].resample('ME').sum()

# calculate annual ablation
mb200['custom_year'] = (mb200.index + pd.offsets.MonthBegin(7)).year
annual_ablation = mb200.groupby('custom_year')['melt'].sum()
annual_ablation.index = pd.to_datetime(annual_ablation.index.astype(str)) + pd.DateOffset(months=7)

### --
# load observational melt rate

#### plotting #####
plt.close('all')
fig, ax = plt.subplots(3,1,num=1,figsize=(14,6))

ax[0].plot(mb200.index,mb200['melt']*1e-3, label='model')
ax[0].set_xlim([mb200.index[0], mb200.index[-1]])
ax[0].grid()
ax[0].set_ylabel('Daily')
# ax[0].set_ylabel('Ablation at MTK [m]')
# mean monthly
ax[1].plot(monthly_sum.index, monthly_sum.values*1e-3, 'o-')
ax[1].grid()
ax[1].set_xlim([mb200.index[0], mb200.index[-1]])
ax[1].set_ylabel('Monthly')

ax[2].stairs(annual_ablation[0:-2]*1e-3, annual_ablation.index[0:-1], baseline=None, label='model')
ax[2].set_xlim([mb200.index[0], mb200.index[-1]])
ax[2].set_ylim(13,22)
ax[2].set_ylabel('Yearly')
ax[2].grid()

plt.savefig('/home/calving/Nextcloud/Moreno_gps/glimb/ablation_96_24.png')


long_term_monthly_mean = monthly_sum.groupby(monthly_sum.index.month).mean()
monthly_anomaly = monthly_sum - monthly_sum.index.map(lambda d: long_term_monthly_mean[d.month])
moving_avg = monthly_anomaly.rolling(window=24, center=True).mean()

# plot monthly anomaly
fig, ax = plt.subplots(1,1,num=2,figsize=(10,4))

ax.bar(monthly_anomaly.index, monthly_anomaly.values*1e-3, width=25, color='gray' )
ax.plot(moving_avg.index, moving_avg.values * 1e-3, color='red', linewidth=2, label='24-Month Moving Average')
ax.grid()
ax.set_xlim([mb200.index[0], mb200.index[-1]])
ax.set_ylim([-1.2, 1.2])
ax.set_ylabel('Monthly')
plt.savefig('/home/calving/Nextcloud/Moreno_gps/glimb/ablation_anomaly_96_24.png')

plt.show()

# show scatter plot
