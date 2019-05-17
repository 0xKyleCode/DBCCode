
# coding: utf-8

# In[291]:


get_ipython().run_line_magic('matplotlib', 'notebook')

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from scipy.signal import boxcar
import glob
from pathlib import Path
import re
import matplotlib
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import itertools
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

sns.set(font_scale=1)
sns.set_style("white")
sns.set_palette('gray')
sns.set_context("paper")

idx=pd.IndexSlice


# In[135]:


#Imports all histograms with filenames as headers



path = "C:/Users/gadzo/OneDrive/Documents/Master Research/Cell Cycle Analysis/Hist_GNP_DTX_Cycle/"

all_files = Path(path)

for p in all_files.glob('*.txt'):
    print(p)
    p.rename(p.with_suffix('.csv'))
    

df = pd.concat(map(lambda file: pd.read_csv(file, sep='\s+').drop(columns=['FL2-A', 'Fluorescence']), all_files.glob('*.csv')), axis=1)


index = [x.stem for x in all_files.glob('*.csv')]
df.columns = index


# In[136]:


##Change the index parameters to fit your labeling scheme

newIndex = pd.DataFrame(columns=['Cell', 'Endo/Exo', 'Cond', 'Time'])


for ind, c in enumerate(index):
    newIndex.loc[ind, 'Cell'] = c[0] 
    newIndex.loc[ind, 'Endo/Exo'] = c[1]
    
    cSplit = re.split('(\d+)', c[2:])
    newIndex.loc[ind, 'Cond'] = cSplit[0]+cSplit[2]
    newIndex.loc[ind, 'Time'] = int(cSplit[1])

newIndex.set_index(['Cell', 'Endo/Exo', 'Cond', 'Time'], inplace=True)
print(newIndex)

df.columns = newIndex.index
df.columns.sortlevel(sort_remaining=True)
df


# In[180]:


s = slice(0,1024)

plt.figure()
plt.plot(df.loc[s, idx['H', 'N':'X', 'D', :]])
plt.show()


# In[5]:


hist['Events'].nonzero()[0][-1]


# In[259]:


def filterDat(data, num=11):
    ones = boxcar(num)/num
    result = np.convolve(data, ones, mode='same')
    
    return result


# In[366]:


def shift(data):
    data = savgol_filter(data.values, 31, 3)
    old_x = np.linspace(0,1023,1024)
    
    # Stretch
    secondIndex =200
    indexes, prop = find_peaks(data, height=5, distance=120)
    print(indexes)
    print(prop)
    
    if indexes.size==2:
        width = 200/(indexes[1]-indexes[0])
        print(width)
        new_x = np.arange(200-(indexes[0]*width), (1024*width+(200-(indexes[0]*width))), width)
        
        if new_x.size>1024:
            new_x = new_x[0:1024]
        new_data = np.interp(old_x, new_x, data)
        
        return new_data/(data.sum()*width)
    
    elif indexes.size==1:
        new_x = old_x*400/indexes[0]
        new_data = np.interp(old_x, new_x, data)
        return new_data/(data.sum()*(400/indexes[0]))
    
        
        return new_data/(data.sum()*width)
    else:
        return data/data.sum()
    """
    difference = secondIndex-secondMaxIndex
    ratio = secondIndex/(secondMaxIndex)
    old_x = np.linspace(0, int(len(data))-1, int(len(data)))
    new_x = np.linspace(0, int(len(data))-1, int(len(data)*ratio))
"""
    


# In[370]:


#df_filt = df.apply(filterDat)
df_sav = df.apply(shift)


# In[367]:


shift(df.loc[s, idx['H', 'X', 'D', 24]])


# In[368]:


plt.figure()
#plt.plot(df.loc[s, idx['H', 'X', 'D', 24]])
plt.plot(shift(df.loc[s, idx['H', 'X', 'D', 24]]))
plt.show()


# In[352]:


s = slice(0,1024)


fig, axes = plt.subplots(figsize=(8, 6))

plt.plot(df_sav.loc[s, idx['M', :, ('C','D'), :]])


axes.legend()

axes.set_ylabel('% of Total')
axes.set_xlabel("DNA content (Arbitrary Units)")
axes.set_xlim(100, 550)
axes.xaxis.set_major_locator(plt.NullLocator())
axes.xaxis.set_major_formatter(plt.NullFormatter())
#axes.set_ylim(0, 100)
axes.set_title("MDA-MB-231 Cell Cycle, 50nM Docetaxel")
plt.show()
plt.savefig('MDA_Cell_Cycle', bbox_inches='tight')


# In[374]:


fig, axes = plt.subplots(1, 4, figsize=(8, 2.5), sharey=True)
fig.suptitle('MDA-MB-231')
axes[0].plot(df_sav.loc[s, idx['M', 'N', 'C', 24]])
axes[0].set_title('Control')
axes[1].plot(df_sav.loc[s, idx['M', 'N', 'D', 8]])
axes[1].set_title('8h')
axes[2].plot(df_sav.loc[s, idx['M', 'N', 'D', 24]])
axes[2].set_title('24h')
axes[3].plot(df_sav.loc[s, idx['M', 'X', 'D', 24]])
axes[3].set_title('Exo 24h')
#fig.subplots_adjust(hspace=0)
for ax in axes:
    ax.set_xlim(50, 550)
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.set_ylim(0, .025)
    ax.label_outer()
    
axes[0].set_ylabel('% of Total')
axes[1].set_xlabel("DNA content")
axes[2].set_xlabel("(Arbitrary Units)")
plt.show()
plt.savefig('MDA_Cell_Cycle.png', bbox_inches='tight', dpi=300, format='png')


# In[152]:


y[137]

