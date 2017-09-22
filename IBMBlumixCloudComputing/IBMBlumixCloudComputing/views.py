import logging
import random
import keystoneclient
import string
import sys
import mimetypes
import time
import re
import pyDes
import urllib3
import os
import flask
import urllib.request as urllib2
import swiftclient.client as swiftclient

from datetime import datetime
from flask import render_template
from werkzeug.utils import secure_filename
from IBMBlumixCloudComputing import app
from flask import Flask, redirect, url_for, request
from os.path import abspath, isabs, isdir, isfile, join

fileName = "defaultFileName"
containerName = "containerName"
url = "https://ibmBluemixURL.com"
authUrl = "https://authURL.com"
projectId = "projectId"
region = "regionName"
userId = "userId",
username = "username"
password = "password"
domainId = "domainId"
domainName = "domainName"
role = "role"
encryptKey = "encryptKey"

conn = swiftclient.Connection(key=password, authurl=authUrl, auth_version=3, os_options={"project_id": projectId, "user_id": userId, "region_name": region})

@app.route('/encryptKey', methods = ['POST'])
def userKey():
    encryptKey = request.value
key = pyDes.des(encryptKey, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad = None, padmode = pyDes.PAD_PKCS5) 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year = datetime.now().year,
    )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.form.get('up', None) == "Upload":
        conn.put_container(containerName)
        file = request.files['thefile']
        fileName = file.filename
        fileContent = file.read()
        encFile = key.encrypt(fileContent)
        conn.put_object(containerName, fileName, contents = encFile, content_type = "text")

    return render_template(
        'index.html',
        title=fileName,
        year = datetime.now().year,
        message='File uploaded to Bluemix cloud:',
        filename = fileName
    )

@app.route('/lstFiles', methods=['GET', 'POST'])
def getListOfFiles():
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            dataFilename = data['name']
    lstFile = "lstFileNames.txt"
    getFile = conn.get_object(containerName, dataFilename)
    with open(lstFile, 'w') as listFile:
        listFile.write(lstFile[1])
    
    return render_template(
        'index.html',
        title='Success',
        year = datetime.now().year,
        message='List downloaded to local system'
    )

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.form.get('down', None) == "Download":
        decFile = conn.get_object(containerName, fileName)
        with open(fileName, 'w') as myFile:
               myFile.write(tostring(decFile[1]).decode("utf-8"))
    return render_template(
        'index.html',
        title='Success',
        year = datetime.now().year,
        message='File downloaded to local system'
    )