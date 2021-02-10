#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:17:35 2020

@author: gauravmohan
"""

from collections import defaultdict
import os
import pandas as pd
from inspect import currentframe, getframeinfo

route_data = {}

'''
This function will look for the routes csv and the daily report, then it will create a dictionary with keys: Routes, values: locations
It will then match the daily report to the routes dictionary and compile the contents of the dictionary for each location
by incrementing the item amount when the item name matches.
'''


def gen_dict(report_name):
    print(report_name)
    check = 0
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir, topdown=False):
        for file in files:
            filepath = subdir + os.sep + file
            name = file.split(".")[0]
            if name == "wholesale1":
                sales_price = pd.read_csv(filepath,header=None,usecols=[1,12],skiprows=1)
                rows2 = len(sales_price.index)
                check += 1
            if name == "Locations" and file.endswith(".csv"):
                check += 1
                routes = pd.read_csv(filepath, header=None, usecols=[1], encoding='UTF-8')
                rows = len(routes.index)
                temp = []
                routes_dict = defaultdict(list)
                for i in range(0, rows):
                    if "Location" in str(routes.iat[i, 0]):
                        temp.append(i)

                for i in range(0, rows):
                    if i in temp:
                        j = i + 1
                        while j not in temp:
                            routes_dict[routes.iat[i, 0].rstrip()].append(
                                str(routes.iat[j, 0]).rstrip().replace(" ", ""))
                            if j + 1 >= rows:
                                break
                            else:
                                j += 1

                check_val = int(len(routes_dict.keys()))
                print(check)
            if file.endswith(".txt") and report_name == name and check == 2:
                lines = []
                with open(filepath, "r") as myfile:
                    first_line = myfile.readline()
                    for line in myfile:
                        if line == first_line:
                            pass
                        else:
                            lines.append(line.strip())
                count = 1
                while count <= check_val:
                    curr_route = "Location"
                    i = 0
                    tracker = 0
                    inner_dict = defaultdict(int)
                    price_dict = defaultdict(float)
                    while i < len(lines):
                        if lines[i] in routes_dict[curr_route]:
                            i += 1
                            while i < len(lines) and len(lines[i]) != 0:
                                try:
                                    main_part = lines[i].split("-->")
                                    val = eval(main_part[2])
                                    inner_dict[val[0]] += val[1]
                                    decimal = round(float(val[2][1:]), 3)
                                    price_dict[val[0]] += decimal
                                    i += 1
                                except NameError:
                                    i += 1

                            tracker += 1
                        if tracker == len(routes_dict[curr_route]):
                            break
                        else:
                            i += 1
                    break


                fdict = {key: (inner_dict[key], price_dict[key]) for key in inner_dict}
                final_dict = sorted(fdict.items(), key=lambda x: x[1], reverse=True)
                report = open("item_sums" + report_name + ".txt", 'w')
                report.write(f'{curr_route}-->{routes_dict[curr_route]}\n')
                for i in final_dict:
                    report.write(str(i) + '\n')
                report.close()
                trans_dict = {}
                total_rev = 0
                total_profit = 0
                for j in range(0, rows2):
                    if sales_price.iat[j,1] == None:
                        j += 1
                    if sales_price.iat[j,1] == 'No Data':
                        j += 1
                    if sales_price.iat[j,1] == 'Cost (Min Price)':
                        j += 1
                    for i in final_dict:
                        revenue = i[1][1]
                        revenue = round(revenue,3)
                        if i[0] == str(sales_price.iat[j,0]).rstrip():
                            profit = revenue-float(i[1][0])*float(sales_price.iat[j,1])
                            trans_dict[i[0]] = ((revenue, profit))
                            total_profit += profit
                            total_rev += revenue

                with open("cost-analysis" + report_name + ".txt","w") as totals:

                    for k,v in trans_dict.items():
                        totals.write(k + ", Total Transaction Amount: $" + str(round(v[0], 3)) + ", Profit: $" + str(round(v[1], 3)) + "\n")
                    totals.write("The total profit is $" + str(round(total_profit,3)) + " and the total transaction amount is $" + str(round(total_rev,3)) + "\n")
                    totals.close()



if __name__ == '__main__':
    report_list = ['biweekly_report','weekly_report','daily_report']
    for i in range(0, len(report_list)):
        report_name = report_list[i]
        gen_dict(report_name)