from global_vars import db


class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))


class Photo(db.Model):
    imageID = db.Column(db.String(16), primary_key=True)
    username = db.Column(db.String(20), db.ForeignKey("user.username"), primary_key=True)
    caption = db.Column(db.String(256))
    userClass = db.Column(db.String(20))
    uploadDate = db.Column(db.Date)

