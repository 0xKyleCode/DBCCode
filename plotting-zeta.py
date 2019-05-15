'''
Make figures for paper
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set(font_scale=1.2)
sns.set_style("whitegrid")
sns.set_style('ticks')
flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]

sns.set_palette(sns.hls_palette(8, l=.3, s=.8))


def smoothData(data):
    num = 15
    ones = np.ones(num)/num
    return np.convolve(data, ones, mode='same')


def plotData(data1, data2, data3, data4):
    """
    plots data
    """
    fig = plt.figure(figsize=(8, 6))
    plt.plot(data3[0][:-1], smoothData(data3[1][:-1]),
             label="15 nm", alpha=0.5)
    plt.fill_between(data3[0][:-1], smoothData(data3[1][:-1]), alpha=0.8)

    plt.plot(data4[0][:-1], smoothData(data4[1][:-1]),
             label="50 nm", alpha=0.5)
    plt.fill_between(data4[0][:-1], smoothData(data4[1][:-1]), alpha=0.8)
    plt.plot(data1[0][:-1], smoothData(data1[1][:-1]),
             label="15 nm+PEG+RGD", alpha=0.5)
    plt.fill_between(data1[0][:-1], smoothData(data1[1][:-1]), alpha=0.8)
    plt.plot(data2[0][:-1], smoothData(data2[1][:-1]),
             label="50 nm+PEG+RGD", alpha=0.5)
    plt.fill_between(data2[0][:-1], smoothData(data2[1][:-1]), alpha=0.8)

    plt.xlabel('Zeta Potential [mV]')
    plt.ylabel('Relative Frequency - Intensity Weighted [%]')
    plt.legend()
    plt.xlim((-80, 80))
    plt.show()


if __name__ == '__main__':
    data1 = openCSV('15+PEG+RGD-Zeta.csv')
    data2 = openCSV('50+PEG+RGD-Zeta.csv')
    data3 = openCSV('15-Zeta.csv')
    data4 = openCSV('50-Zeta.csv')
    plotData(data1, data2, data3, data4)
