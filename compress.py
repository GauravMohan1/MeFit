#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 12:08:50 2020

@author: gauravmohan
"""

from collections import defaultdict
import os
import pandas as pd
from inspect import currentframe, getframeinfo
from error import compress

route_data = {}
checklist = []
'''
This function will look for the routes csv and the daily report, then it will create a dictionary with keys: Routes, values: locations
It will then match the daily report to the routes dictionary and compile the contents of the dictionary for each location
by incrementing the item amount when the item name matches.
'''


def gen_dict():
    check = 0
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir, topdown=False):
        for file in files:
            filepath = subdir + os.sep + file
            name = file.split(".")[0]
            if name == "Routes" and file.endswith(".csv"):
                check += 1
                routes = pd.read_csv(filepath, header=None, usecols=[1], encoding='UTF-8')
                rows = len(routes.index)
                temp = []
                routes_dict = defaultdict(list)
                for i in range(0, rows):
                    try:
                        if len(str(routes.iat[i, 0])) == 3:
                            raise ValueError("There is an empty cell in the Routes csv at row " + str(i + 1))
                    except Exception as e:
                        checklist.append((type(e).__name__, str(e), getframeinfo(currentframe()).lineno))
                        break
                    if "Route" in str(routes.iat[i, 0]):
                        temp.append(i)

                for i in range(0, rows):
                    if i in temp:
                        j = i + 1
                        while j not in temp:
                            routes_dict[routes.iat[i, 0].rstrip()].append(str(routes.iat[j, 0]).rstrip().replace(" ",""))
                            if j + 1 >= rows:
                                break
                            else:
                                j += 1
                check_val = int(len(routes_dict.keys()))
                print(routes_dict)
            if file.endswith(".txt") and "daily" in name and check == 1:
                lines = []
                with open(filepath, "r") as myfile:
                    first_line = myfile.readline()
                    for line in myfile:
                        if line == first_line:
                            pass
                        else:
                            lines.append(line.strip())
                if "nan" in lines:
                    print("There is a missing line in your csv data files")
                count = 1
                while count <= check_val:
                    curr_route = f'Route {count}'
                    i = 0
                    tracker = 0
                    inner_dict = defaultdict(int)
                    while i < len(lines):
                        if lines[i] in routes_dict[curr_route]:
                            i += 1
                            while i < len(lines) and len(lines[i]) != 0:
                                try:
                                    main_part = lines[i].split("-->")
                                    val = eval(main_part[2])
                                    inner_dict[val[0]] += val[1]
                                    i += 1
                                except NameError:
                                    i += 1


                            tracker += 1
                        if tracker == len(routes_dict[curr_route]):
                            break
                        else:
                            i += 1
                    final_dict = sorted(inner_dict.items(), key=lambda x: x[1], reverse=True)
                    report = open("routetotal.txt", 'a')
                    report.write(f'{curr_route}-->{routes_dict[curr_route]}\n')
                    for i in final_dict:
                        report.write(str(i) + '\n')
                    report.write('\n')
                    count += 1

                report.close()
                return


if __name__ == '__main__':
    gen_dict()
    compress(checklist)