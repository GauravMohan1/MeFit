#!/usr/bin/env python3
# -*- coding: utf -*-

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import pandas as pd
import shutil
from inspect import currentframe, getframeinfo
from error import grab_mappings

checklist = []

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Authenticate if they're not there

    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})

    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    try:
        gauth.Authorize()
    except Exception as e:
        checklist.append((type(e).__name__,str(e),getframeinfo(currentframe()).lineno))

# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

MIMETYPES = {
        # Drive Document files as MS dox
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Drive Sheets files as MS Excel files.
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        # Drive presentation as MS pptx
        'application/vnd.google-apps.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        # see https://developers.google.com/drive/v3/web/mime-types
    }
EXTENSTIONS = {
        'application/vnd.google-apps.document': '.docx',
        'application/vnd.google-apps.spreadsheet': '.xlsx',
        'application/vnd.google-apps.presentation': '.pptx'
}

f = open("failed.txt","w+")
#Set the folder_id to the folder in your G-Drive that you want to download
folder_id = '14QbjRBlvs9jU7lr3OUx8tupohwonpbED'
root = 'MachineInfo'

try:
    os.mkdir(root)
except FileExistsError:
    #if the directory drive-download exists, the folder will be removed and then re-created
    shutil.rmtree(root)
    os.mkdir(root)

def escape_fname(name):
    return name.replace('/','_')
'''
For each file in the folder you set, if the file mimetypes match the MIMETYPE dictionary, then
the excel files should download the contents and convert them to the a csv file. Files that have shortcuts
attached to the file in the folder_id (e.g. a spreadsheet that is a shortcut) will fail to download.
'''
def search_folder(folder_id, root):
    all_files = []
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
    for file in file_list:
        all_files.append(file)
        if file['mimeType'].split('.')[-1] == 'folder':
            foldername = escape_fname(file['title'])
            create_folder(root,foldername)
            search_folder(file['id'], '{}{}/'.format(root,foldername))
        else:
            download_mimetype = None
            filename = escape_fname(file['title'])
            filename = '{}{}'.format(root,filename)
            try:
                print('DOWNLOADING:', filename)
                if file['mimeType'] in MIMETYPES:
                    download_mimetype = MIMETYPES[file['mimeType']]

                    file.GetContentFile(filename+EXTENSTIONS[file['mimeType']], mimetype=download_mimetype)
                else:
                    file.GetContentFile(filename)
            except:
                print('FAILED')
                f.write(filename+'\n')
    convert_files(all_files)

def create_folder(path,name):
    os.mkdir('{}{}'.format(path,escape_fname(name)))


'''
This is specific to an excel file that has multiple sheets that need to be converted to
individual csv files. Each sheet will be renamed to the sheet name and converted to a csv.
You have to set the path to the path where your mapping-routes folder is created.
'''

def convert_files(all_files):
    #set the path of your mapping-routes
    path = "/Users/gauravmohan/Documents/PycharmProjects/MeFit/PyDrive/MachineInfo"
    for file in all_files:
        if "Routes" == file['title']:
            #converts the routes excel to a csv
            data_xls = pd.read_excel(path+'/Routes.xlsx')
            data_xls.to_csv(path+'/Routes.csv', encoding='utf-8')
        elif "Inventory" in file['title']:
            mapping_sheets = pd.ExcelFile(path + '/Inventory.xlsx')
            sheetnames = mapping_sheets.sheet_names
            for i in sheetnames:
                # for each sheet in an excel, this will parse it and convert each sheet to a csv
                if "REMOVED" not in i:
                    sheet = mapping_sheets.parse(i)
                    sheet.to_csv(path + '/' + i.replace(" ", "") + ".csv")
        elif "Locations" == file['title']:
            #converts the routes excel to a csv
            data_xls = pd.read_excel(path+'/Locations.xlsx')
            data_xls.to_csv(path+'/Locations.csv', encoding='utf-8')
        elif "Min-Max_Price_Check" == file['title']:
            data_xls = pd.read_excel(path + '/Min-Max_Price_Check.xlsx')
            data_xls.to_csv(path + '/Min-Max_Price_Check.csv', encoding='utf-8')
        elif "Machine" in file['title']:
            mapping_sheets = pd.ExcelFile(path+'/Machine-Mapping.xlsx')
            sheetnames = mapping_sheets.sheet_names
            for i in sheetnames:
                #for each sheet in an excel, this will parse it and convert each sheet to a csv
                if "REMOVED" not in i:
                    print('hi')
                    sheet = mapping_sheets.parse(i)
                    sheet.to_csv(path+'/'+i.replace(" ","") + ".csv")



try:
    search_folder(folder_id,root+'/')
except Exception as e:
    checklist.append((type(e).__name__, str(e), getframeinfo(currentframe()).lineno))

f.close()
grab_mappings(checklist)
