'''
Make figures for paper
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns
sns.set(font_scale=1.2)
sns.set_style("whitegrid")
sns.set_style('ticks')
sns.set_palette(sns.diverging_palette(255, 133, l=60, n=4, center="dark"))


def openCSV(file):
    """
    opens and returns a csv file contents
    """
    firstColumn = []
    secondColumn = []
    with open(file, 'rt') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if(len(row) != 0 and len(row) != 1):
                if(is_number(row[0])):
                    if(is_number(row[1])):
                        firstColumn.append(float(row[0]))
                        secondColumn.append(float(row[1]))

    return [firstColumn, secondColumn]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def plotData(data1, data2, data3, data4, data5, data6):
    """
    plots data
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    """    plt.bar(data1[0][:-1], data1[1][:-1], width=np.diff(data1[0]),
            ec='none', align='edge', label="15 nm GNPs", alpha=0.5)
    plt.xscale("log")
    plt.title("Size Distrubution")
    plt.xlabel('Paritlcle Diameter [nm]')
    plt.ylabel('Relative Frequency - Intensity Weighted [%]')
    plt.legend()

    plt.bar(data2[0][:-1], data2[1][:-1], width=np.diff(data2[0]),
            ec='none', align='edge', label="15 nm+PEG", alpha=0.5)
    plt.xscale("log")
    plt.title("Size Distrubution")
    plt.xlabel('Paritlcle Diameter [nm]')
    plt.ylabel('Relative Frequency - Intensity Weighted [%]')
    plt.legend()
    """
    ax.bar(data3[0][:-1], data3[1][:-1], width=np.diff(data3[0]),
           ec='none', align='edge', label="15 nm+PEG+RGD", alpha=0.5)
    ymax = max(data3[1][:-1])
    xpos = data3[1][:-1].index(ymax)
    xmax = data3[0][:-1][xpos]

    ax.annotate('{:.2f} nm'.format(xmax), xy=(
        xmax, ymax), xytext=(xmax-8, ymax+.1))

    """   plt.bar(data4[0][:-1], data4[1][:-1], width=np.diff(data1[0]),
            ec='none', align='edge', label="50 nm GNPs", alpha=0.5)
    plt.xscale("log")
    plt.title("Size Distrubution")
    plt.xlabel('Paritlcle Diameter [nm]')
    plt.ylabel('Relative Frequency - Intensity Weighted [%]')
    plt.legend()

    plt.bar(data5[0][:-1], data5[1][:-1], width=np.diff(data2[0]),
            ec='none', align='edge', label="50 nm+PEG", alpha=0.5)
    plt.xscale("log")
    plt.title("Size Distrubution")
    plt.xlabel('Paritlcle Diameter [nm]')
    plt.ylabel('Relative Frequency - Intensity Weighted [%]')
    plt.legend()"""

    ax.bar(data6[0][:-1], data6[1][:-1], width=np.diff(data6[0]),
           ec='none', align='edge', label="50 nm+PEG+RGD", alpha=0.5)
    ymax = max(data6[1][:-1])
    xpos = data6[1][:-1].index(ymax)
    xmax = data6[0][:-1][xpos]

    ax.annotate('{:.2f} nm'.format(xmax), xy=(
        xmax, ymax), xytext=(xmax-10, ymax+.1))

    ax.set_xscale("log")
    ax.set_xlabel('Particle Diameter [nm]')
    ax.set_ylabel('Relative Frequency - Intensity Weighted [%]')
    ax.legend()

    ax.set_xlim((0, 1000))
    plt.show()


if __name__ == '__main__':
    data1 = openCSV('15-DLS.csv')
    data2 = openCSV('15+PEG-DLS.csv')
    data3 = openCSV('15+PEG+RGD-DLS.csv')
    data4 = openCSV('50-DLS.csv')
    data5 = openCSV('50+PEG-DLS.csv')
    data6 = openCSV('50+PEG+RGD-DLS.csv')
    plotData(data1, data2, data3, data4, data5, data6)
