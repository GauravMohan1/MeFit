#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import shutil


rootdir = os.getcwd()
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        folder_name = subdir.split("/")[-1]
        print(folder_name)
        try:
            if folder_name == "drive_download":
                shutil.rmtree(subdir)
            elif folder_name == "drive_download_weekly":
                shutil.rmtree(subdir)
            elif folder_name == "MachineInfo":
                shutil.rmtree(subdir)
            elif folder_name == "Graphs":
                shutil.rmtree(subdir)
            elif folder_name == "analysis_reports":
                shutil.rmtree(subdir)
            elif folder_name == "sales_reports":
                shutil.rmtree(subdir)
            elif folder_name == "error_reports":
                shutil.rmtree(subdir)
        except FileNotFoundError:
            pass

        if file.endswith(".txt"):
            try:
                name = file.split(".txt")[0]
                if name == "daily_report":
                    os.remove(file)
                elif name == "weekly_report":
                    os.remove(file)
                elif name == "biweekly_report":
                    os.remove(file)
                elif name == "cost-analysisdaily_report":
                    os.remove(file)
                elif name == "cost-analysisweekly_report":
                    os.remove(file)
                elif name == "cost-analysisbiweekly_report":
                    os.remove(file)
                elif name == "item_sumsdaily_report":
                    os.remove(file)
                elif name == "item_sumsweekly_report":
                    os.remove(file)
                elif name == "item_sumsbiweekly_report":
                    os.remove(file)
                elif name == "slot_price_error":
                    os.remove(file)
                elif name == "slot_price_error_weekly":
                    os.remove(file)
                elif name == "slot_price_error_biweekly":
                    os.remove(file)
                elif name == "price_range_error":
                    os.remove(file)
                elif name == "price_range_error_weekly":
                    os.remove(file)
                elif name == "price_range_error_biweekly":
                    os.remove(file)
                elif name == "routetotal":
                    os.remove(file)
                elif name == "pubd_report":
                    os.remove(file)
                elif name == "pubw_report":
                    os.remove(file)
                elif name == "pubi_report":
                    os.remove(file)
            except FileNotFoundError:
                pass

        if file.endswith(".zip"):
            try:
                name = file.split(".zip")[0]
                if name == "Graphs":
                    os.remove(file)
                elif name == "error_reports":
                    os.remove(file)
                elif name == "sales_reports":
                    os.remove(file)
                elif name == "analysis_reports":
                    os.remove(file)
            except FileNotFoundError:
                pass




