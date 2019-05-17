'''
Make figures for paper
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns
import itertools
sns.set(font_scale=1.2)
sns.set_style("white")
sns.set_palette(sns.diverging_palette(255, 133, l=60, n=6, center="dark"))


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


def plotData(data1, data2, data3, data4):
    """
    plots data
    """
    fig = plt.figure(figsize=(8, 6))
    normalized = []
    minVal = min(data1[1])
    maxVal = max(data1[1])
    for x in data1[1]:
        normalized.append((x-minVal)/(maxVal-minVal))

    fifteen = plt.plot(data1[0], normalized, lw='2', label=r'15 nm GNP')

    normalized = []
    minVal = min(data3[1])
    maxVal = max(data3[1])
    for x in data3[1]:
        normalized.append((x-minVal)/(maxVal-minVal))

    fifty = plt.plot(data3[0], normalized, lw='2',
                     label=r'15 nm GNP+PEG+RGD')

    normalized = []
    minVal = min(data2[1])
    maxVal = max(data2[1])
    for x in data2[1]:
        normalized.append((x-minVal)/(maxVal-minVal))

    fifty = plt.plot(data2[0], normalized, lw='2', label=r'50 nm GNP')

    normalized = []
    minVal = min(data4[1])
    maxVal = max(data4[1])
    for x in data4[1]:
        normalized.append((x-minVal)/(maxVal-minVal))
    fifty = plt.plot(data4[0], normalized, lw='2',
                     label=r'50 nm GNP+PEG+RGD')

    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Absorption [AU]')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    data1 = openCSV('15nm.csv')
    data2 = openCSV('50nm.csv')
    data3 = openCSV('15+PEG+RGD.csv')
    data4 = openCSV('50+PEG+RGD.csv')
    plotData(data1, data2, data3, data4)
