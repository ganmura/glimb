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


# sum up discharge for all elevation and show time series.
path = hd + '/Nextcloud/fortran/glimb/output/'
names = [os.path.basename(x) for x in glob.glob(path + 'mb*perito_moreno.csv')]
names.sort()
# unit mm for each elevation band
merged_discharge = pd.DataFrame()

dataframes = []

# load hypsometry
hypso = pd.read_csv(hd + '/Nextcloud/fortran/glimb/input/hypsometry_moreno.csv')

# Loop through all files in the directory
for file in names:
    file_path = os.path.join(path, file)
    
    # Read the file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Extract only the necessary columns (e.g., 'yr', 'doy', 'discharge')
    discharge_data = df[['yr', 'doy', 'discharge']]
    
    discharge_data['date'] = discharge_data.apply(lambda row: datetime(int(row['yr']), 1, 1) + timedelta(days=int(row['doy']) - 1), axis=1)

    dataframes.append(discharge_data['discharge'])

#TODO need to think for multi year output
daily_discharge = []
daily_disch_elev = []
#TODO here we need tank model to estimate discharge
for i, x in enumerate(dataframes[0]): # loop for day
    dmy = []
    for j in range(0,len(dataframes),1): # loop for elevation band
        disch_vol = (hypso.values[j][1]*1e6) * (dataframes[j][i].item()/1e3)
        dmy.append(disch_vol)  # Start with the first DataFrame

    daily_discharge.append(np.sum(dmy))
    daily_disch_elev.append(dmy)

daily_discharge=np.array(daily_discharge)
daily_disch_elev=np.array(daily_disch_elev)

### 
plt.close('all')
fig, axs = plt.subplots(2, 1, figsize=(12, 8), num=1)
# total runoff
axs[0].plot(discharge_data['date'], daily_discharge*1e-6,'-k')
axs[0].set_ylabel('Glacier-wide discharge [Mt/day]')
axs[0].grid()
# axs[0].set_yscale('log')

# runoff at each elevation range
cmap = plt.get_cmap('brg')  # Choose a colormap, e.g., 'viridis', 'plasma', 'inferno', etc.
for i in range(0,np.shape(daily_disch_elev)[1]):
    color = cmap(i / np.shape(daily_disch_elev)[1])
    axs[1].plot(discharge_data['date'], daily_disch_elev[:,i]*1e-6,'-',color=color,label=str(round(hypso.values[i,0])))

axs[1].set_ylabel('Discharge at each elevation [Mt/day]')
axs[1].grid()
axs[1].legend(ncol=3)
# axs[1].set_yscale('log')

# save glacier wide discharge
# Create a DataFrame
data = pd.DataFrame({
    'date': discharge_data['date'],
    'discharge_Mt_d': daily_discharge*1e-6
})

# Save to CSV
output_path = hd + '/Nextcloud/Moreno_gps/glimb/glacier_wide_discharge.csv'
data.to_csv(output_path, index=False)

# save plot
plt.savefig(hd + '/Nextcloud/Moreno_gps/glimb/discharge.png', dpi=300)
plt.show()