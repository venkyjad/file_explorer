# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, redirect, request,json
from filesystem import Folder, File
from action import *
from flask import request
from os import error
from flask.json import jsonify

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    FILES_ROOT=os.path.dirname(os.path.abspath(__file__)),
)

#Loads the index page
@app.route('/')
def index(path=''):
    return render_template('index.html')

#Using AngularJS we get all the list of files and send in json format
@app.route('/getfilelist',methods=['GET','POST'])
def getfilelist(path='templates'):#path can be mentioned here or passed as a parameter

    app.config.update(
        DEBUG=True,
        FILES_ROOT=os.path.dirname(os.path.abspath(__file__)),
    )
    path = ''
    path_join = os.path.join(app.config['FILES_ROOT'], path)
    if os.path.isdir(path_join):
        folder = Folder(app.config['FILES_ROOT'], path)
        folder.read()
        filename = []

        for file in folder.files:
            cdict = {}
            cdict['filen']=file.name
            cdict['filepath']=file.path
            filename.append(cdict)
        for folder in folder.folders:
            mdict={}
            mdict['foldname']=folder.name
            mdict['foldpath']=folder.path

            filename.append(mdict)
        print filename
        return jsonify(files = filename)


#Gets All the Subfiles in the folder
@app.route('/get_subfiles',methods=['GET','POST'])
def get_subfiles():
    data = json.loads(request.data.decode())
    path = data['filepath']
    app.config.update(
        DEBUG=True,
        FILES_ROOT=os.path.dirname(os.path.abspath(__file__)),
    )
    path_join = os.path.join(app.config['FILES_ROOT'], path)
    if os.path.isdir(path_join):
        folder = Folder(app.config['FILES_ROOT'], path)
        folder.read()
        filename = []

        for file in folder.files:
            cdict = {}
            cdict['filen']=file.name
            cdict['filepath']=file.path
            filename.append(cdict)
        for folder in folder.folders:
            mdict={}
            mdict['foldname']=folder.name
            mdict['foldpath']=folder.path

            filename.append(mdict)
        return jsonify(subfiles = filename)

#This reads the content in a particular file
@app.route('/view_content/<path:path>')
def view_content(path=''):
    print "hello"

    app.config.update(
        DEBUG=True,
        FILES_ROOT=os.path.dirname(os.path.abspath(__file__)),
    )
    path_join = os.path.join(app.config['FILES_ROOT'], path)
    my_file = File(app.config['FILES_ROOT'], path)
    context = my_file.apply_action(View)
    folder = Folder(app.config['FILES_ROOT'], my_file.get_path())
    if context == None:
        return render_template('file_unreadable.html', folder=folder)
    return render_template('file_view.html', text=context['text'], file=my_file, folder=folder)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
