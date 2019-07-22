from flask import Flask
import os
import torch
from PIL import Image
from torchvision.transforms import transforms
import argparse
from pycocotools.coco import COCO
import pickle
import gensim
import json
from flask import request
import pymysql
import urllib
import time
from stanfordcorenlp import StanfordCoreNLP
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
import api as API
from global_vars import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/photobook"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

CORS(app, supports_credentials=True)
db.init_app(app)
# encoder = Encoder(256)
# decoder = Decoder(256, 512, 11560, 1)
dictionary = None
nlp = None
transform = transforms.Compose([transforms.RandomCrop(224),
                                    transforms.RandomHorizontalFlip(),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))])

image_idr = 'E:\\apache-tomcat-8.5.38\\webapps\\images\\'
size = 256


@app.route('/test', methods=['GET', 'POST'])
def test():
    print('path-test')
    if request.method == 'POST':
        print('POST Request')
        userid = request.form.get('userid')
        print(userid)
        a = [1, 2, 3]
        res = json.dumps({'list' : a})
        return res
    else:
        userid = request.values.get('userid')
        print(userid)
        a = [1, 2, 3]
        res = json.dumps(a)
        return res


@app.route('/server/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())
    username = data['username']
    password = data['password']
    res = API.login(username, password)
    return res


@app.route('/server/register', methods=['POST'])
def register():
    data = json.loads(request.get_data())
    username = data['username']
    password = data['password']
    res = API.register(username, password)
    return res


@app.route('/server/upload', methods=['POST'])
def upload():
    username = request.form.get('username')
    userClass = request.form.get('userClass')
    image = request.files.get("file")
    if image is None:
        return "failed"
    res = API.upload(username, userClass, image)
    return res


@app.route('/server/getCategories')
def getCategories():
    username = request.values.get('username')
    res = API.getCategories(username)
    return res


@app.route('/server/allImages')
def getAllImages():
    username = request.values.get('username')
    res = API.getAllImages(username)
    return res


@app.route('/server/modifyPhoto', methods=['POST'])
def modifyPhoto():
    data = json.loads(request.get_data())
    username = data['username']
    imageID = data['imageID']
    category = data['userClass']
    res = API.modifyInfo(username, imageID, category)
    return res


@app.route('/server/delete', methods=['POST'])
def deletePhoto():
    data = json.loads(request.get_data())
    username = data['username']
    imageID = data['imageID']
    res = API.deletePhoto(username, imageID)
    return res


@app.route('/server/searchByWords', methods=['POST'])
def searchByWords():
    data = json.loads(request.get_data())
    username = data['username']
    tags = data['tags']
    res = API.searchByWords(username, tags)
    return res


@app.route('/server/searchByPhoto', methods=['POST'])
def searchByPhoto():
    username = request.form.get('username')
    image = request.files.get('file')
    res = API.searchByPhoto(username, image)
    return res


@app.route('/server/classifyAll', methods=['POST'])
def classifyAll():
    data = json.loads(request.get_data())
    username = data['username']
    tags = json.loads(data['tags'])
    res = API.classifyAll(username, tags)
    return res


@app.route('/server/info')
def getInfo():
    username = request.values.get('username')
    res = API.getInfo(username)
    return res


@app.route('/server/batchUpdate', methods=['POST'])
def batchUpdate():
    data = json.loads(request.get_data())
    username = data['username']
    json_str = data['tags']
    json_object = json.loads(json_str)
    tags = json_object['tags']
    ids = json_object['ids']
    res = API.batchUpdate(username, tags, ids)
    return res
    

if __name__ == '__main__':
    app.run()

