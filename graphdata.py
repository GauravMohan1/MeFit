#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:35:49 2020

@author: gauravmohan
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

'''
today = date.today()
fdate = str(date.today())
current_date = fdate.replace("-", "")
'''


def generate_graph(location_name):
    df = pd.read_csv('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/drive_download_weekly/merged7.csv', usecols=[0, 6, 8, 9, ])

    if os.path.isfile('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/' + str(location_name) + '.csv'):
        df2 = pd.read_csv('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/' + location_name + '.csv', usecols=[1])

    else:
        print("File dosen't exist")
        return '0'

    column_names = ["Machine No.", "Price", "No. Items", "Date"]
    df.columns = column_names
    df["Transaction Amount"] = df["Price"] * df["No. Items"]

    key = df2.iat[0, 0]
    if len(key) == 0:
        return '0'

    RowCount = len(df.index)
    ColumnCount = len(df.columns)

    RowCount2 = len(df2.index)
    ColumnCount2 = len(df2.columns)

    df = df[df["Machine No."] == key]
    if df.empty:
        return '0'
    aggregation_functions = {'Transaction Amount': 'sum'}
    df = df.groupby(df['Date']).aggregate(aggregation_functions).reset_index()

    df.plot(x='Date', y='Transaction Amount', kind='bar', figsize=(10, 10), title=key, ylim=(0, 50))

    nfile = location_name + "GRAPH.png"
    return nfile

def add_to_graphs(files):
    folder_name = "Graphs"
    folder = os.path.join('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/', folder_name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i in files:
        if i.split('.')[1] == 'png':
            filename = i.format(folder_name)
            file = os.path.join(folder, filename)
            plt.savefig(file)


if __name__ == '__main__':
    files = []
    location_list = []
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            name = file.split('.')[0]
            if name == "Locations" and filepath.endswith(".csv"):
                locs = pd.read_csv(filepath, usecols=[1], na_filter=False)
                rows = len(locs.index)
                for i in range(0, rows):
                    if len(locs.iat[i, 0]) == 0:
                        decrement = rows - i
                        rows = rows - decrement
                        break
                for i in range(0, rows):
                    location_list.append(str(locs.iat[i, 0]).replace(" ", ""))
    for i in range(0, len(location_list)):
        location_name = location_list[i]
        if generate_graph(location_name) != '0':
            files.append(generate_graph(location_name))

    add_to_graphs(files)



