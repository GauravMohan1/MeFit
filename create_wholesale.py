#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 14:12:17 2020

@author: varunmeduri
"""
import shutil
import os 

root = 'Inventory'

try:
    os.mkdir(root)

except FileExistsError:
    #if the directory drive-download exists, the folder will be removed and then re-created
    shutil.rmtree(root)
    os.mkdir(root)
    
list_of_files = ['/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/Bottles.csv', '/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/Cans.csv',
                 '/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/CoffeeOfficeSupplies.csv', '/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/Snacks.csv',
                 '/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo/RefrigeratedFrozen.csv']
for i in list_of_files:
    shutil.move(i, 'Inventory')