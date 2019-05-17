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


def plotData(*arg):
    """
    plots data
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    for item in arg:
        data = item[0]
        name = item[1]
        ax.bar(data[0][:-1], data[1][:-1], width=np.diff(data[0]),
               ec='none', align='edge', label=name, alpha=0.5)
        ymax = max(data[1][:-1])
        xpos = data[1][:-1].index(ymax)
        xmax = data[0][:-1][xpos]

        ax.annotate('{:.2f} nm'.format(xmax), xy=(
            xmax, ymax), xytext=(xmax-8, ymax+.1))

    ax.set_xscale("log")
    ax.set_xlabel('Particle Diameter [nm]')
    ax.set_ylabel('Relative Frequency - Intensity Weighted [%]')
    ax.legend()
    ax.set_xlim((0, 1000))
    plt.show()


if __name__ == '__main__':
    data1 = [openCSV('test_files/DLS/15-DLS.csv'), "15 nm"]
    data2 = [openCSV('test_files/DLS/15+PEG-DLS.csv'), "15 nm+PEG"]
    data3 = [openCSV('test_files/DLS/15+PEG+RGD-DLS.csv'), "15 nm+PEG+RGD"]
    plotData(data1, data2, data3)
