from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import time
import datetime
import sys, os
from flaskblog.secrets_poster import decryptor

#initializes google sheets api thingy
def gacc_init():
    SCOPE = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    try:# Try to get absolute location of json file for linux
        location = os.path.abspath(os.path.dirname(sys.argv[0]))+"//" + "secret.json"
        SECRETS_FILE = location
        print("Initializing sheets...Please wait...")
        print(location)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)
    except:
        try:# Try to get absolute location of json file for windows
            location = os.path.abspath(os.path.dirname(sys.argv[0]))+"\\" + "secret.json"
            SECRETS_FILE = location
            print("Initializing sheets...Please wait...")
            print(location)
            credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)      
        except:# if it fails ask user to provide it instead
            print("Couldn't find json location.")
            location = input("Please specify absolute location of your json: ")
            SECRETS_FILE = location
            print("Initializing sheets...Please wait...")
            credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)
    gc = gspread.authorize(credentials)
    print("Sheet initialization done")
    return gc

#Gets all data from the first sheet
def create_frame(gc ,SPREADSHEET):
    workbook = gc.open(SPREADSHEET)
    #1 is used to indicate the first of your available sheets  as printed by the list_available function
    sheet = workbook.sheet1
    data = pd.DataFrame(sheet.get_all_records())
    return data, sheet

#Gets censor dictionary from the third sheet    
def get_censor_dict(gc ,SPREADSHEET):
    workbook = gc.open(SPREADSHEET)
    sheet = workbook.get_worksheet(2)
    data = pd.DataFrame(sheet.get_all_records())
    return data
    
#Gets settings from encrypted url that leads to the second sheet
def get_settings(gc):
    url = decryptor.decrypt('ENCRYPTED URL GOES HERE')
    workbook = gc.open_by_url(url)
    sheet = workbook.get_worksheet(1)    
    token_encrypted = sheet.cell(1, 2).value
    page_id = sheet.cell(2, 2).value
    spreadsheet_name = sheet.cell(3, 2).value
    return token_encrypted,page_id,spreadsheet_name

#Marks whether the secret was uploaded or archived (1 or 0)
def mark_uploaded(entry, bin_value, sheet):
    sheet.update_cell(entry, 6, bin_value)

#Marks the time and date that the secret was posted
def mark_timestamp(entry, sheet):
    sheet.update_cell(entry, 4, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#Adds to the sheet the actual (maybe edited) posted "secret"
def save_posted(entry, posted, sheet):
    sheet.update_cell(entry, 5, posted)

#Finds the first empty cell in order to count how many "secrets" are left
def find_empty_cell(data):
    i = 1
    try:
        while True:
            if (data['School'][i] == "None"):
                print("break")
                break            
            i+=1
    except:
        return (i) 
    return (i) 

#The find_entry functions finds the first empty cell in the binary 
#column of the spread sheet and begins work from that point
def find_entry(data):
    i = 0
    while True:
        if((data['Binary'][i] != 0) and (data['Binary'][i] != 1)):
            break
            
        i+=1
    return i

#Gets current hashtag and prints it
def show_hashtag(data, entry):
    index = entry-1
    while (data['Hashtag'].iat[index]==''):
        index = index -1
    print("Current Hashtag is: ", data['Hashtag'].iat[index])
    return data['Hashtag'].iat[index]

#Writes posted hashtag to sheet when a post is made 
def write_hashtag(entry, msg, sheet):
    sheet.update_cell(entry, 3, msg)
