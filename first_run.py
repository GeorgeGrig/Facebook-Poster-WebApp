##########################SECRETS POSTER STUFF
from flaskblog.secrets_poster import  wrapper,main

def inintial_values():
    data, entry, api, worksheet,max_entry = wrapper.initialize()  
    if (entry!=0):
        cur_hash = wrapper.sheet.show_hashtag(data, entry)
    elif(entry==0):
        cur_hash = input('Input your new hashtag: ')
        print("Since it is the first time you are using the code with the given form, don't forget to post at least one secret!")
    henum = main.find_henum(data, cur_hash)
    Queue = max_entry - entry + 1
    Posted = 0
    
    return cur_hash,henum,data,entry,worksheet,api,Queue,Posted
