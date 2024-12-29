import pandas as pd
import numpy  as np 
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
import platform
import os
import glob

if platform.system()=='Darwin':
    hd = '/Users/ameghino/'
elif platform.system()=='Linux':
    hd = '/home/calving/'

fn = hd + '/Nextcloud/fortran/glimb/output/sumup_moreno'
names = [os.path.basename(x) for x in glob.glob(fn + '*.csv')]
names.sort()

plt.close('all')
fig, axs = plt.subplots(4, 4, figsize=(12, 8), num=1)

for year in names:
    yr = year[12:-4]
    df = pd.read_csv(fn + yr + '.csv', sep=",")

    cnt = 0
    for ax in axs:
        for a in ax:
            a.plot(df['elevation']/1e3, df[df.columns[cnt+1]],'-', label= yr)
            a.set_ylabel(df.columns[cnt+1])
            a.set_xlabel('z [km]')
            cnt += 1

plt.legend()
plt.tight_layout()
plt.savefig(hd + '/Nextcloud/Moreno_gps/glimb/sumup_year.png', dpi=300)
plt.show()

