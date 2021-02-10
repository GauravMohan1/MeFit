#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:50:40 2020

@author: varunmeduri
"""


from collections import defaultdict
import pandas as pd
import os
from datetime import date
import time
from inspect import currentframe, getframeinfo
from error import mefitpublicbiweekly
zero_day = []
tracker = 0
count = 0
check = 0
checklist = []
today = date.today()
fdate = str(date.today())
current_date = fdate.replace("-", "")
xl = pd.ExcelFile('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/Machine-Mapping.xlsx')
num_of_mapping_files = len(xl.sheet_names)

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
report = open(f"biweekly_report.txt", 'a')
report.write("(This report was generated at " + str(current_time) + " on " + str(today) + ')\n')
report.close()

'''
Route function looks through all the files in the Mefit directory, 
assigns the file with the list of locations to a pandas dataframe data3, 
assigns the file with the current dates transaction report to a pandas dataframe data1,
checks to see if all values in the report are != 0,
calls find_file function with data1, data3 as inputs
'''
def route():
    global check
    rootdir = os.getcwd()
    #walks through all files in local directory
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            name = file.split(".csv")[0]
            #finds the location list file and the transaction data report
            if name == "Locations":
                data3 = pd.read_csv(filepath,usecols=[1],na_filter=False)
                rows = len(data3.index)
                for i in range(0,rows):
                    if len(data3.iat[i,0]) == 0:
                        decrement = rows - i
                        rows = rows - decrement
                        break
                check += 1
            if name == "Min-Max_Price_Check":
                locs = []
                data4 = pd.read_csv(filepath,usecols=[1,2,3])
                rows2 = len(data4.index)
                for i in range(0,rows2):
                    locs.append(str(data4.iat[i,0]).rstrip())
                check += 1
            if name == "merged":
                data1 = pd.read_csv(filepath, header=None, usecols=[0, 5, 6, 8, 9, 10])
                numrows = len(data1.index)
                for i in range(0, numrows):
                    try:
                        if data1.iat[i, 3] == 0:
                            raise ValueError("No. items purchased reported as 0 at row " + str(i))
                            #print("Error in transaction report No. items purchased reported as 0")
                    except Exception as e:
                        checklist.append((type(e).__name__, str(e), getframeinfo(currentframe()).lineno))
                check += 1
            if check == 3:
                find_file(data3, data1, rows, data4,rows2,locs)

'''
looks through the list of locations and finds the csv file for the individual mapping sheet
reads the mapping file into the pandas dataframe data2
calls read data with data1 and data2 as inputs
'''
def find_file(data3, data1, rows,data4,rows2,locs):
    done = 0
    global tracker, num_of_mapping_files
    rootdir = os.getcwd()
    #looking through all files in local directory
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".csv"):
                #narrowing down the search to csv only files
                name = file.split(".csv")[0]
                for i in range(0, rows):
                    location = data3.iat[i, 0].replace(" ", "")
                    #matching the location from the list of locations to the corresponding slot mapping sheet
                    if name == location:
                        tracker += 1
                        data2 = pd.read_csv(filepath, usecols = [1,2,3,4])
                        if data2['Identity'].count() == 0:
                            break
                        else:
                            check_name = str(data2.iat[1, 0])
                            check_name = check_name.replace(" ", "")
                        if tracker < num_of_mapping_files:
                            read_data(data1, data2, location,rows, check_name,data4,rows2,locs)
                        else:
                            done += 1
                            break
                if done == 1:
                    break

'''
creates an initial dict containing slots as the keys and item names as the values
checks if slot and machine number match, if it does adds to the main dictionary me_data
if slot already exists in me_data item total is added to the previous instance of the slot in the dictionary
writes per location data to a txt file in the local directory called daily report that gets appended each cycle 
'''
def read_data(data1, data2, location,rows, check_name,data4,rows2,locs):
    global count, zero_day
    #global count
    initial_dict = {}
    me_data = defaultdict(dict)
    RowCount = len(data1.index)
    RowCount2 = len(data2.index)
    for i in range(0, RowCount2):
        initial_dict[data2.iat[i, 1]] = [data2.iat[i, 2],data2.iat[i,3]]  # initial_dict creates a key of slots to a value of item name
    for i in range(0, RowCount):
        try:
            if data1.iat[i, 3] == 0:
                print("Error in transaction report No. items purchased reported as 0")
        except:
            pass
        for k, v in initial_dict.items():  # initial dict is used to create the inner dictionary
            # if the slot matches from the two data files and the machine number/location are the same as inputted
            # and the slots is alr in me_data then traverse through it and add the item to the nested dictionary
            if data1.iat[i, 1][1:] == (str)(k) and data1.iat[i, 0] == data2.iat[0, 0] and data1.iat[i, 1][1:] in me_data[data2.iat[0, 0]] and location == check_name:
                inner_copy = me_data[data2.iat[0, 0]].copy()
                for slot, item in inner_copy.items():
                    if data1.iat[i,1][1:] == slot:
                        if item[0] in locs:
                            for j in range(0, rows2):
                                if str(data4.iat[j, 0]).rstrip() == item[0] and (float(data1.iat[i, 2]) < float(data4.iat[j, 1]) or float(data1.iat[i, 2]) > float(data4.iat[j, 2])):
                                    with open("price_range_error_biweekly.txt", 'a') as error_file:
                                        error_file.write(item[0] + " at location "+ location + " has a price of " + str(data1.iat[i, 2]) + " which is outside of price range." + "\n")
                                        error_file.close()
                                        break
                        decimal = float(item[2][1:]) + float(data1.iat[i, 2]) * float(data1.iat[i, 3])
                        cost = round(decimal, 3)
                        me_data[data1.iat[i, 0]][data1.iat[i, 1][1:]] = ((item[0], item[1] + data1.iat[i, 3], "$" + str(cost)))
                        # me_data --> {machine id:{slot info: ((item,count of how many times item has shown up))}}
            elif data1.iat[i, 1][1:] == (str)(k) and data1.iat[i, 0] == data2.iat[0, 0] and location == check_name:
                if float(data1.iat[i,2]) != float(v[1]):
                    with open("slot_price_error_biweekly.txt", 'a') as errors:
                        errors.write("The transaction price does not match the mapping price at slot " + str(k) + " at line " + str(i+1) + " at " + location + "\n")
                        errors.close()
                decimal = float(data1.iat[i, 2]) * float(data1.iat[i, 3])
                cost = round(decimal, 3)
                me_data[data1.iat[i, 0]][data1.iat[i, 1][1:]] = ((v[0], data1.iat[i,3], "$" + str(cost)))
            else:
                if str(k) not in zero_day:
                    with open("zero-day.txt","a") as zeroday:
                        zeroday.write(str(k)+"\n")
                        zeroday.close()
                    zero_day.append(str(k))
                # if the slot item is not in the inner dictionary then set the freq of the item to 1
    if count < rows:
        count += 1
        report = open(f"biweekly_report.txt", 'a')
        if count == 1:
            report.write("Biweekly report for " + str(data1.iat[0,4]) + " to " + str(data1.iat[RowCount - 1, 4]) + "\n")
        report.write(location + '\n')
        for i,j in me_data.items():
            for k,v in sorted(j.items()):
                report.write(f'{i}-->{k}-->{v}\n')
        report.write('\n')
        report.close()

        new_report = open(f"pubi_report.txt", 'a')
        new_report.write(location + '\n')
        for i, j in me_data.items():
            for k, v in sorted(j.items()):
                new_report.write(f'{i}-->{k}-->{v[0]}-->#Items-->{v[1]} (Price:${float(v[2][1:])/v[1]}, Total:{v[2]})\n')
        new_report.close()


if __name__ == '__main__':
    route()
    mefitpublicbiweekly(checklist)