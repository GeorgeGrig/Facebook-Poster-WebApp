from flaskblog.secrets_poster import sheet,fb_autoposter,decryptor
import pandas
import time

def initialize():
    gc = sheet.gacc_init()
    sheet.list_available(gc)
    print('-------------------------')    
    try:#Tries to get page id  and fb api key (and decrypt it) from the google sheet
        token_encrypted,page_id,spreadsheet = sheet.get_settings(gc)
        key = decryptor.decrypt(token_encrypted)
    except:# if it fails, asks user to provide it instead
        print("Couldn't read api key.")
        key = input("Input your facebook user access api key: ")
        print("Couldn't read page id.")
        page_id = input("Please specify page id: ")   
    #Gets all the data from the work sheet and stores it in "data"
    data, worksheet = sheet.create_frame(gc ,spreadsheet)
    
    #Autoposter initialization 
   
    print("Initializing facebook poster... Please wait....")
    cfg = fb_autoposter.init_token(key,page_id)
    api = fb_autoposter.get_api(cfg)
    print("Facebook Initialization Done")
    print("-------------------------")

    #Autoposter Initialization
    
    #Entry Initialization
    
    print("Looking for Entry....")
    entry = sheet.find_entry(data)
    print("Entry Found, number of entry is: ", entry+2)
    max_entry = sheet.find_empty_cell(data)
    print("Post left to do: " + str(max_entry - (entry+1)))

    #Entry Initialization

    return data, entry, api, worksheet, max_entry

#Used to check whether the "secret" has a url in it

def url_checker(str):
   i = 0 
   if "www." in str:
       i = 1
   if "WWW." in str:
       i = 1  
   if "https:" in str:
       i = 1      
   if "http:" in str:
       i = 1   
   if ".com" in str:
       i = 1 
   if ".gr" in str:
       i = 1 
   if "@gmail" in str:
       i = 1 
   if "@outlook" in str:
       i = 1 
   if ".be" in str:
       i = 1 
   if "docs." in str:
       i = 1 
   return i    

