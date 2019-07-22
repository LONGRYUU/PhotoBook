from flask_sqlalchemy import SQLAlchemy
from models import User, Photo
import time
import os
from global_vars import db, model, nlp, encoder, decoder, transform, dictionary
from pymysql.err import *
import json
import similarityMethods as Sims
import classification as Classify
import pymysql
from infer import infer
from resizer import resize_image

image_dir = 'E:\\nginx-1.16.0\\static\\images'


def makeImageName():
    t = int(time.time() * 1000000)
    return str(t)
    

def generate(username, imageID):
    
    caption = infer(encoder, decoder, dictionary['value'], transform, imageID)
    return caption

def login(username, password):
    user = User.query.get(username)
    if user == None:
        return "invalid username"
    elif user.password == password:
        return "success"
    else:
        return "wrong password"


def register(username, password):
    print(username, password)
    user = User(username=username, password=password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return "invalid username"
    path = os.path.join(image_dir, username)
    os.mkdir(path)
    return "success"


def upload(username, userClass, image):
    uploadDate = time.strftime("%Y-%m-%d", time.localtime())
    imageID = makeImageName()
    
    fileName = os.path.join(image_dir, username, imageID + '.jpg')
    image.save(fileName)
    
    tempName = os.path.join(image_dir, username, 'rsz' + imageID + '.jpg')
    resize_image(fileName, tempName, 256)
    
    caption = generate(username, tempName)
    photo = Photo(imageID=imageID, username=username, userClass=userClass, caption=caption, uploadDate=uploadDate)
    
    try:
        db.session.add(photo)
        db.session.commit()
    except Error:
        res = {'result': 'failed'}
        os.remove(fileName)
        os.remove(tempName)
        return json.dumps(res)

    res = {'result': 'success', 'imageID': imageID, 'category': userClass, 'uploadDate':uploadDate, 'caption':caption}
    return json.dumps(res)


def getCategories(username):
    sql = "select distinct userClass from photo where username='"+ username +"'"
    res = db.session.execute(sql)
    data = res.fetchall()
    data = [item[0] for item in data]
    if 'default' not in data:
        data.append('default')
    return json.dumps(data)


def getAllImages(username):
    rows = db.session.query(Photo).filter_by(username=username).all()
    timeMap = {}
    cateMap = {}
    imageMap = {'categories':[], 'imageIDs':[], 'captions':[]}
    for (i, photo) in enumerate(rows):
        imageMap['categories'].append(photo.userClass)
        imageMap['imageIDs'].append(photo.imageID)
        imageMap['captions'].append(photo.caption)
        date = str(photo.uploadDate)
        cate = str(photo.userClass)
        if date in timeMap:
            timeMap[date].append(i)
        else:
            timeMap[date] = [i]
        if cate in cateMap:
            cateMap[cate].append(i)
        else:
            cateMap[cate] = [i]
        
    res = {'imageMap':imageMap, 'timeMap':timeMap, 'cateMap':cateMap}
    return json.dumps(res)


def modifyInfo(username, imageID, category):
    photo = Photo.query.get((imageID, username))
    photo.userClass = category
    try:
        db.session.commit()
    except Error:
        return "failed"
    return "success"


def deletePhoto(username, imageID):
    photo = Photo.query.get((imageID, username))
    try:
        db.session.delete(photo)
        db.session.commit()
    except Error:
        return "failed"
    fileName = os.path.join(image_dir, username, imageID + '.jpg')
    os.remove(fileName)
    tempName = os.path.join(image_dir, username, 'rsz' + imageID + '.jpg')
    os.remove(tempName)
    return "success"

def searchByWords(username, words, threshold=0.4):
    rows = db.session.query(Photo).filter_by(username=username).all()
    sentences = [photo.caption for photo in rows]

    res = {'imageIDs': [], 'captions':[]}

    if len(sentences) > 0:
        similarities = Sims.tfidf(words, sentences, model)
        imageIDs = [photo.imageID for photo in rows]
        captions = [photo.caption for photo in rows]
        paths = [item for item in zip(similarities, imageIDs, captions) if item[0] > threshold]
        paths.sort(key=lambda x:x[0], reverse=True)
        res['imageIDs'] = [item[1] for item in paths]
        res['captions'] = [item[2] for item in paths]
    
    res['query'] = words
    res = json.dumps(res)
    return res


def searchByPhoto(username, image):
    imageID = 'temp' + makeImageName() 
    
    fileName = os.path.join(image_dir, username, imageID + '.jpg')
    image.save(fileName)
    
    tempName = os.path.join(image_dir, username, 'rsz' + imageID + '.jpg')
    resize_image(fileName, tempName, 256)
    
    caption = generate(username, tempName)
    print(caption)
    res = searchByWords(username, caption, threshold=0.6)
    os.remove(fileName)
    os.remove(tempName)
    return res


def classifyAll(username, tags):
    rows = db.session.query(Photo).filter_by(username=username).all()
    captions = [photo.caption for photo in rows]
    imageIDs = [photo.imageID for photo in rows]
    dic = {tag: [] for tag in tags}
    # res['<OTHER>'] = []
    similarities = Classify.classifyByAttr(tags, captions, model)
    
    for i in range(len(captions)):
        idx = similarities[i][0]
        if idx < 0:
            # res['<OTHER>'].append((imageIDs[i], 0))
            continue
        else:
            dic[tags[idx]].append((imageIDs[i], similarities[i][1], captions[i]))
            # ids[tags[idx]].append((imageIDs[i], similarities[i][1], captions[i]))
    ids = {}
    caps = {}
    for key in dic:
        dic[key].sort(key=lambda x:x[1], reverse=True)
        ids[key] = [item[0] for item in dic[key]]
        caps[key] = [item[2] for item in dic[key]]

    res = {'ids':ids, 'caps':caps}
    res = json.dumps(res)
    return res


def getInfo(username):
    res = {'date':'', 'cate':'', 'freq':''}
    sql = "with C as (select userClass, count(*) as num from photo X where username='"+username+"' group by userClass)" + \
                " select userClass from C as A where Not exists(select userClass from C as B where B.num > A.num)"

    data = db.session.execute(sql).fetchall()
    res['cate'] = data[0][0]
    sql = "with C as (select uploadDate, count(*) as num from photo where username='"+username+"' group by uploadDate)" + \
                " select uploadDate from C as A where Not exists(select uploadDate from C as B where B.num > A.num)"
    data = db.session.execute(sql).fetchall()
    res['date'] = str(data[0][0])

    rows = db.session.query(Photo).filter_by(username=username).all()
    images = [photo.imageID for photo in rows]
    captions = [str(photo.caption) for photo in rows]

    freqs = Classify.word_count(captions, images, nlp)
    freqs = sorted(freqs.items(), key=lambda x:len(x[1]), reverse=True)
    freqs = [{'word': t[0], 'images':t[1]} for t in freqs]

    res['freq'] = json.dumps({'default':freqs})
    res = json.dumps(res)
    return res
   

def batchUpdate(username, tags, ids):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='photobook')
    cur = conn.cursor()
    values = [(tag, username, imageID) for tag in tags for imageID in ids[tag]]
    try:
        num = cur.executemany("update photo set userClass=%s where username=%s and imageID=%s", values)
        print(num)
        conn.commit()
    except Error:
        conn.rollback()
        print(Error)
        return "failed"
    if num != len(values):
        conn.rollback()
        return "failed"
    cur.close()
    conn.close()
    return"success"