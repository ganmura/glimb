import pandas as pd
import numpy  as np 
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
import platform

if platform.system()=='Darwin':
    hd = '/Users/ameghino/'
elif platform.system()=='Linux':
    hd = '/home/calving/'
    
fn = hd + '/Nextcloud/fortran/glimb/output/sumup_moreno'
year = '2020-2020'
df = pd.read_csv(fn + year + '.csv', sep=",")

cnt = 0
fig, axs = plt.subplots(4, 4, figsize=(12, 8), num=1)
for ax in axs:
	for a in ax:
		a.plot(df['elevation']/1e3, df[df.columns[cnt+1]],'-k')
		a.set_ylabel(df.columns[cnt+1])
		a.set_xlabel('z [km]')
		cnt += 1

plt.tight_layout()
plt.show()

