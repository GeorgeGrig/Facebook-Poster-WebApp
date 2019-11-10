from flaskblog.secrets_poster import wrapper,fb_autoposter

def move_to_archive(worksheet,entry):
    wrapper.sheet.mark_uploaded(entry+2, 0, worksheet)
    wrapper.sheet.mark_timestamp(entry+2, worksheet)
    print("Moved to archive :(")

def post_anom(worksheet,entry,answer,api,cur_hash):
    #Posts to page using fb api
    fb_autoposter.post_msg(answer, api)
    print("Posted!")
    #Updates values to sheets
    wrapper.sheet.mark_uploaded(entry+2, 1, worksheet)
    wrapper.sheet.mark_timestamp(entry+2, worksheet)
    answer = answer.split(None, 1)[1]
    wrapper.sheet.save_posted(entry+2, answer, worksheet)
    wrapper.sheet.write_hashtag(entry+2, cur_hash, worksheet)
    
def find_henum(data, cur_hash):
    try:
        print("Current Hashtag enumeration is: ",data['Hashtag'].value_counts()[cur_hash])
        henum = data['Hashtag'].value_counts()[cur_hash]
    except(KeyError):
        print("New hashtag typed!")
        henum = 0              
    return henum     #current hashtag number

def admin_edit_add(answer,admin_edit):
    answer_piece = answer.rsplit('(', 1)[1]
    answer = answer.rsplit('(', 1)[0]
    answer = answer + "[αδμιν εδιτ]: " + admin_edit + "\n\n" + "(" + answer_piece    
    return answer

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
