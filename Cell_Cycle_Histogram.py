
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter


# In[2]:


idx=pd.IndexSlice

path = "C:/Users/gadzo/OneDrive/Documents/Master's Research/Cell cycle/Aaron/Aaron Kristy Cell Cycle Nob/"

DTX_C = pd.read_csv(path+"MDA DTX Hist/MDA DTX Ctl.csv").drop('Fluorescence', axis=1)
DTX_2 = pd.read_csv(path+"MDA DTX Hist/MDA DTX 2hr.csv").drop('Fluorescence', axis=1)
DTX_8 = pd.read_csv(path+"MDA DTX Hist/MDA DTX 8hr.csv").drop('Fluorescence', axis=1)
DTX_D = pd.read_csv(path+"MDA DTX Hist/MDA DTX DMSO.csv").drop('Fluorescence', axis=1)

DTX_C2 = pd.read_csv(path+"MDA DTX_1 Hist/MDA DTX_1 Ctl.csv").drop('Fluorescence', axis=1)
DTX_4 = pd.read_csv(path+"MDA DTX_1 Hist/MDA DTX_1 4hr.csv").drop('Fluorescence', axis=1)
DTX_4_24 = pd.read_csv(path+"MDA DTX_1 Hist/MDA DTX_1 4_24hr.csv").drop('Fluorescence', axis=1)
DTX_24 = pd.read_csv(path+"MDA DTX_1 Hist/MDA DTX_1 24hr.csv").drop('Fluorescence', axis=1)


# In[3]:


x = slice(0,1024)
plt.figure()
plt.plot(DTX_4_24['FL2-A'][x], DTX_4_24['Events'][x])
plt.plot(DTX_24['FL2-A'][x], DTX_24['Events'][x])
plt.show()


# In[279]:


c = filterDat(DTX_C2['Events'])
h = DTX_C2['FL2-A'].values



plt.plot(h[200:350],c[200:350])
plt.show()


# In[4]:


hist = DTX_4_24
#x = slice(hist['Events'].nonzero()[0][0]-1, hist['Events'].nonzero()[0][-1]+1)
x = slice(hist['Events'].nonzero()[0][0]-3, 300)
p = [31, 41, 51]

yhat1 = savgol_filter(hist[x]['Events'].values, p[0], 3, mode='interp') # window size 51, polynomial order 3
yhat2 = savgol_filter(hist[x]['Events'].values, p[1], 3, mode='interp') # window size 51, polynomial order 3
yhat3 = savgol_filter(hist[x]['Events'].values, p[2], 3, mode='interp') # window size 51, polynomial order 3

plt.figure()
plt.plot(hist[x]['FL2-A'], yhat1, label=p[0])
plt.plot(hist[x]['FL2-A'], yhat2, label=p[1])
plt.plot(hist[x]['FL2-A'], yhat3, label=p[2])
plt.plot(hist[x]['FL2-A'], hist[x]['Events'], label='raw')
plt.legend()
plt.show()


# In[81]:


hist = DTX_4_24
x = slice(hist['Events'].nonzero()[0][0]-1, hist['Events'].nonzero()[0][-1]+1)
#x = slice(hist['Events'].nonzero()[0][0]-1, 300)
p = [11, 21, 31]

yhat1 = filterDat(hist['Events'][x], p[0])
yhat2 = filterDat(hist['Events'][x], p[1])
yhat3 = filterDat(hist['Events'][x], p[2])

plt.figure()
plt.plot(hist[x]['FL2-A'], yhat1, label=p[0])
plt.plot(hist[x]['FL2-A'], yhat2, label=p[1])
plt.plot(hist[x]['FL2-A'], yhat3, label=p[2])
plt.plot(hist[x]['FL2-A'], hist[x]['Events']/hist[x]['Events'].max()*100, label='raw')
plt.legend()
plt.show()


# In[5]:


hist['Events'].nonzero()[0][-1]


# In[14]:


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns
import itertools
import pandas as pd
import scipy
from scipy.signal import savgol_filter
from scipy.signal import find_peaks_cwt
from scipy.signal import boxcar
sns.set(font_scale=1.2)
sns.set_style("white")
sns.set_palette('husl')


# In[15]:


def filterDat(data, num=11):
    ones = boxcar(num)/num
    result = np.convolve(data, ones, mode='same')
    
    return result

def Savgol(data, num=41):
    u = slice(data.nonzero()[0][0]-3, data.nonzero()[0][-1])
    v = savgol_filter(data[u].values, num, 3)
    
    result = np.zeros(1024)
    result[u]=v
    print(result.size)
    return result
    


# In[16]:


def shift(data):
   
    # Stretch
    secondIndex =200
    indexes = find_peaks_cwt(data, np.arange(10, 100))
    peaks = data[indexes]
    print(indexes)
    print(peaks)
    # find max of indexes
    firstMaxIndex = indexes[peaks.argmax()]
    peaks[peaks.argmax()]=-1
    secondMaxIndex = indexes[peaks.argmax()]
    print(peaks)
    
    print(firstMaxIndex, secondMaxIndex)
    width = 200/(secondMaxIndex-firstMaxIndex)
    #print(width)
    new_x = np.arange(200-(firstMaxIndex*width), (1024*width+(200-(firstMaxIndex*width))), width)
    if len(new_x)!=1024:
        new_x = new_x[0:1024]
    """
    difference = secondIndex-secondMaxIndex
    ratio = secondIndex/(secondMaxIndex)
    old_x = np.linspace(0, int(len(data))-1, int(len(data)))
    new_x = np.linspace(0, int(len(data))-1, int(len(data)*ratio))
"""
    #new_data = np.interp(new_x, old_x, data)
    
    norm = data/(data.sum()*width)
    print(norm.sum()*width)
    return new_x, norm


# In[17]:


fig, axes = plt.subplots(figsize=(8, 6))

y = Savgol(DTX_C['Events'])
x, y = shift(y)
axes.plot(x, y, label="Control")

"""y = Savgol(DTX_2['Events'])
x, y = shift(y)
axes.plot(x, y, label="2 hour")
axes.fill_between(x, y, alpha=0.1)
"""

y = Savgol(DTX_4['Events'])
x, y = shift(y)
axes.plot(x, y, label="4 hour")

y = Savgol(DTX_8['Events'])
x, y = shift(y)
axes.plot(x, y, label="8 hour")

y = Savgol(DTX_4_24['Events'])
x, y = shift(y)
axes.plot(x, y, label="28 hour")
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


# In[164]:


fig, axes = plt.subplots(figsize=(8, 6))



y = Savgol(DTX_4_24['Events'])
axes.plot(y)
#x, y = shift(y)
#axes.plot(x, y, label="28 hour")
#axes.fill_between(x, y, alpha=0.1)
axes.legend()
axes.set_xlim(100,300)

plt.show()


# In[152]:


y[137]

