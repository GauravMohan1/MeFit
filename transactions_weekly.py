#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 13:46:32 2020

@author: gauravmohan
"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from datetime import date


today = date.today()
fdate = str(date.today())
current_date = fdate.replace("-", "")
first_day = (int)(current_date[-2:])
first_month = (int)(current_date[-4:-2])
first_year = (int)(current_date[:4])
count = 0
if first_day < 7:
    count = 7-first_day
string_first = current_date[-4:-2]
if first_month != 1:
    prev_month = first_month - 1
else:
    prev_month = 12
calender_dict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
days_left = calender_dict[prev_month] - count
gauth = GoogleAuth()
num_files = 7
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Authenticate if they're not there

    # This is what solved the issues:
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})

    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:

    # Refresh them if expired

    gauth.Refresh()
else:

    # Initialize the saved creds

    gauth.Authorize()

# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")  

drive = GoogleDrive(gauth)


MIMETYPES = {
        # Drive Document files as MS dox
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        # Drive Sheets files as MS Excel files.
        'application/vnd.google-apps.spreadsheet': 'text/csv',
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
folder_id = '1nDrKx-kwcV-L-JpKrTohNT0qN1nt853i'
root = 'drive_download_weekly'

try:
    os.mkdir(root)
except FileExistsError:
    pass
file_list = drive.ListFile({'q': "'1nDrKx-kwcV-L-JpKrTohNT0qN1nt853i' in parents and trashed=false"}).GetList()


def escape_fname(name):
    return name.replace('/','_')

def search_folder(folder_id, root):
    global num_files, prev_month, first_day, string_first, first_month, days_left
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
    new_file_list = []
    for file in file_list:
        date = file['title'].split('-')[4]
        day = (int)(date[-2:])
        month = (int)(date[-4:-2])
        year = (int)(date[:4])
        if first_month == 1:
            if first_day < 7 and year == first_year:
                if day > 0 and day <= first_day and month == first_month:
                    new_file_list.append(file)
                    day -= 1
                    num_files -= 1
                elif month == prev_month and day > days_left and year == first_year-1:
                    new_file_list.append(file)
            else:
                benchmark = first_day - 7
                if day <= first_day and month == first_month and day > benchmark and year == first_year:
                    new_file_list.append(file)  
        elif first_day < 7 and year == first_year:
            if day > 0 and day <= first_day and month == first_month:
                new_file_list.append(file)
                day -= 1
                num_files -= 1
            elif month == prev_month and day > days_left:
                new_file_list.append(file)
        else:
            benchmark = first_day - 7
            if day <= first_day and month == first_month and day > benchmark and year == first_year:
                new_file_list.append(file)
    
    print(new_file_list)
    download_files(new_file_list,root)


def download_files(new_file_list,root):
    for file in new_file_list:
        if file['mimeType'].split('.')[-1] == 'folder':
            print("Nice")
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
                    print("Yes!")
                    download_mimetype = MIMETYPES[file['mimeType']]

                    file.GetContentFile(filename+EXTENSTIONS[file['mimeType']], mimetype=download_mimetype)
                else:
                    file.GetContentFile(filename)
            except:
                print('FAILED')
                f.write(filename+'\n')

def create_folder(path,name):
    try:
        os.mkdir('{}{}'.format(path,escape_fname(name)))
    except FileExistsError:
        return

search_folder(folder_id,root+'/')

f.close() 
