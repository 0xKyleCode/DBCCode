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
colors = ["#95a5a6", "amber"]
sns.set_palette(sns.color_palette())

hr_24 = np.loadtxt("MDA DTX_1 4_24hr.txt", skiprows=1)
ctl = np.loadtxt("MDA DTX_1 Ctl.txt", skiprows=1)
hr_4 = np.loadtxt("MDA DTX_1 4hr.txt", skiprows=1)
# hr_2 = np.loadtxt("MDA-DTX-#2hr.txt", skiprows=1)
hr_8 = np.loadtxt("MDA DTX 8hr.txt", skiprows=1)
dmso = np.loadtxt("MDA DTX DMSO.txt", skiprows=1)


def filterDat(data):
    num = 9
    ones = boxcar(num)/num
    result = np.abs(np.convolve(data, ones, mode='same'))
    return np.interp(result, (result.min(), result.max()), (0, 100))


def shift(data):
    """
    firstIndex = 200
    index = np.argmax(data)
    if index < firstIndex:
        data = np.insert(data, 0, np.zeros(
            firstIndex-index))[:-(firstIndex-index)]
    elif index > firstIndex:
        data = data[index-firstIndex:]
        data = np.insert(data, len(data)-1, np.zeros(index-firstIndex))
    """
    # Stretch
    secondIndex = 400
    indexes = find_peaks_cwt(data, np.arange(1, 100))

    # find max of indexes
    peaks = data[indexes]
    secondMax = 0
    lastPeak = 0
    for x in range(len(peaks)):
        if peaks[x] < 95.0:
            if peaks[x] > lastPeak:
                lastPeak = peaks[x]
                secondMax = x
    secondMaxIndex = indexes[secondMax]

    difference = secondIndex-secondMaxIndex
    ratio = secondIndex/(secondIndex-difference)
    old_x = np.linspace(0, int(len(data))-1, int(len(data)))
    new_x = np.linspace(0, int(len(data))-1, int(len(data)*ratio))

    new_data = np.interp(new_x, old_x, data)

    return new_data, np.linspace(0, int(len(new_x))-1, int(len(new_x)))


fig, axes = plt.subplots(figsize=(8, 6))

filterData = filterDat(ctl[:, 2])
y, x = shift(filterData)
axes.plot(x, y, label="Control", color='black')
axes.fill_between(x, y, alpha=0.3)

"""filterData = filterDat(hr_4[:, 2])
y, x = shift(filterData)
axes.plot(x, y, label="4 hour")
axes.fill_between(x, y, alpha=0.3)
filterData = filterDat(hr_8[:, 2])
y, x = shift(filterData)
axes.plot(x, y, label="8 hour")
axes.fill_between(x, y, alpha=0.3)
"""
filterData = filterDat(hr_24[:, 2])
y, x = shift(filterData)
axes.plot(x, y, label="24 hour", color='maroon')
axes.fill_between(x, y, alpha=0.3)
axes.legend()

axes.set_ylabel('% of Max')
axes.set_xlabel('Fluorescence')
axes.set_xlim((0, 800))
plt.show()
