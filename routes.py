from flask import (render_template, url_for, flash,redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.secrets_poster.forms import PostForm
from flaskblog.secrets_poster import first_run,main
from wtforms.fields import Label
from pymemcache.client import base
posts = Blueprint('posts', __name__)
client = base.Client(('localhost', 11211))

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    global cur_hash,henum,data,entry,worksheet,api,Queue,Posted
    cur_hash,henum,data,entry,worksheet,api,Queue,Posted = first_run.inintial_values()
    text = ('#' + cur_hash + str(henum+1) + ": " + data['Say your name friend'].iat[entry] + "\n \n" + data['School'].iat[entry])
    date = data['Χρονική σήμανση'][entry]
    form = PostForm()
    if main.url_checker(text):
        has_url = "Yep"
    else: 
        has_url = "Nop"
    #form.title.data = date #changes data
    form.content.data = text #changes data
    date = "Date: "+ date + "  ||  " + "Has link: "+ str(has_url) +"  ||  " + "Queue: "+ str(Queue) + "  ||  " + "Posted: " + str(Posted)
    form.content.label = Label("content", date)
    form.hashtag.data = cur_hash #changes data
    if form.validate_on_submit():
        if form.post.data:
            flash("Posted post on posting poster page :'D "+ cur_hash + str(henum+1), 'success')
            print ("Posted post on posting poster page :'D "+ cur_hash + str(henum+1))
            text = form.content.raw_data[0]
            if form.admin_edit.raw_data[0]:
                text = main.admin_edit_add(text,form.admin_edit.raw_data[0])
            main.post_anom(worksheet,entry,text,api,cur_hash)
            entry += 1
            henum += 2   
            Queue -= 1
            Posted += 1
            return redirect(url_for('posts.next_post'))
        elif form.archive.data:
            flash('Moved to archive :(', 'success')
            print ('Moved to archive :(')
            main.move_to_archive(worksheet,entry)
            entry += 1
            Queue -= 1
            return redirect(url_for('posts.next_post')) 
        elif form.change_hashtag.data:
            if cur_hash != form.hashtag.raw_data[0]:
                henum = 1 
                cur_hash = form.hashtag.raw_data[0] 
                print (cur_hash)
                return redirect(url_for('posts.next_post'))                
    return render_template('create_post.html', title='Secrets Poster',form=form, legend='Post some stuffs')

@posts.route("/post/next", methods=['GET', 'POST'])
@login_required
def next_post():
    global cur_hash,henum,data,entry,worksheet,api,Queue,Posted
    text = ('#' + cur_hash + str(henum) + ": " + data['Say your name friend'].iat[entry] + "\n \n" + data['School'].iat[entry])
    date = data['Χρονική σήμανση'][entry]
    form = PostForm()
    if main.url_checker(text):
        has_url = "Yep"
    else: 
        has_url = "Nop"
    #form.title.data = date #changes data
    form.content.data = text #changes data
    date = "Date: "+ date + "  ||  " + "Has link: "+ str(has_url) +"  ||  " + "Queue: "+ str(Queue) + "  ||  " + "Posted: " + str(Posted)
    form.content.label = Label("content", date)
    form.content.data = text #changes data
    form.hashtag.data = cur_hash #changes data
    if form.validate_on_submit():
        if form.post.data:
            flash("Posted post on posting poster page :'D "+ cur_hash + str(henum), 'success')
            print ("Posted post on posting poster page :'D "+ cur_hash + str(henum))
            text = form.content.raw_data[0]
            if form.admin_edit.raw_data[0]:
                text = main.admin_edit_add(text,form.admin_edit.raw_data[0])
            main.post_anom(worksheet,entry,text,api,cur_hash)
            entry += 1
            henum += 1 
            Queue -= 1
            Posted += 1           
            return redirect(url_for('posts.next_post'))
        elif form.archive.data:
            flash('Moved to archive :(', 'success')
            print ('Moved to archive :(')
            main.move_to_archive(worksheet,entry)
            entry += 1
            Queue -= 1
            return redirect(url_for('posts.next_post'))     
        elif form.change_hashtag.data:
            if cur_hash != form.hashtag.raw_data[0]:
                henum = 1 
                cur_hash = form.hashtag.raw_data[0] 
                print (cur_hash)
                return redirect(url_for('posts.next_post'))                 
    return render_template('create_post.html', title='Secrets Poster',form=form, legend='Post some stuffs')
