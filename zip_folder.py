#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:38:18 2020

@author: varunmeduri
"""

import os
import zipfile
import shutil

def create_folders():
    rootdir = os.getcwd()
    error_reports = ['slot_price_error', 'slot_price_error_weekly', 'slot_price_error_biweekly', 'price_range_error', 'price_range_error_weekly', 'price_range_error_biweekly']
    sales_reports = ['routetotal', 'pubd_report', 'pubw_report', 'pubi_report']
    analysis_reports = ["cost-analysisdaily_report", "cost-analysisweekly_report", "cost-analysisbiweekly_report", "item_sumsdaily_report", "item_sumsweekly_report", "item_sumsbiweekly_report"]
    folder_name = 'error_reports'
    folder = os.path.join('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/', folder_name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i in error_reports:
        filename = (i + ".txt")
        try:
            print(filename)
            file = os.path.join(folder, filename)
            shutil.move('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/' + filename, file)
        except FileNotFoundError:
            pass
    '''
    folder_name1 = 'sales_reports'
    folder1 = os.path.join('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/', folder_name1)
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    for i in sales_reports:
        filename = (i + ".txt")
        try:
            print(filename)
            file = os.path.join(folder1, filename)
            shutil.move('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/' + filename, file)
        except FileNotFoundError:
            pass
    '''
    folder_name2 = 'analysis_reports'
    folder2 = os.path.join('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/', folder_name2)
    if not os.path.exists(folder2):
        os.makedirs(folder2)
    for i in analysis_reports:
        filename = (i + ".txt")
        try:
            print(filename)
            file = os.path.join(folder2, filename)
            shutil.move('/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/' + filename, file)
        except FileNotFoundError:
            pass





# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):

  # setup file paths variable
  filePaths = []

  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for filename in files:
        # Create the full filepath by using os module.
        filePath = os.path.join(root, filename)
        filePaths.append(filePath)

  # return all paths
  return filePaths


# Declare the main function
def main():
    create_folders()

    folder_list = ['/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/Graphs', '/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/error_reports','/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/analysis_reports']
    for i in folder_list:
# Assign the name of the directory to zip
        dir_name = i
  # Call the function to retrieve all files and folders of the assigned directory
        filePaths = retrieve_file_paths(dir_name)
          # printing the list of all files to be zipped
        print('The following list of files will be zipped:')
        for fileName in filePaths:
            print(fileName)
        zip_file = zipfile.ZipFile(dir_name+'.zip', 'w')
        with zip_file:
            for file in filePaths:
                  zip_file.write(file)

        print(dir_name+'.zip file is created successfully!')


# Call the main function
if __name__ == "__main__":
  main()
