from datetime import datetime

from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    trips = db.relationship('Trip', backref='rider', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end = db.Column(db.DateTime)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    vibrations = db.relationship('Vibration', backref='trip', lazy='dynamic')
    gps = db.relationship('GPS', backref='trip', lazy='dynamic')
    imus = db.relationship('IMU', backref='trip', lazy='dynamic')

    def __repr__(self):
        return '<Trip {}>'.format(self.name)


class Vibration(db.Model):
    time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    intensity = db.Column(db.Integer)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))

    def __repr__(self):
        return '<Vibration at {} with intensity>'.format(self.time, self.intensity)


class GPS(db.Model):
    time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))

    def __repr__(self):
        return '<Location at {} with lat={} and lng={}>'.format(self.time, self.latitude, self.longitude)


class IMU(db.Model):
    time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    acceleration_x = db.Column(db.Float)
    acceleration_y = db.Column(db.Float)
    acceleration_z = db.Column(db.Float)
    gyroscope_x = db.Column(db.Float)
    gyroscope_y = db.Column(db.Float)
    gyroscope_z = db.Column(db.Float)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))

    def __repr__(self):
        return '<IMU at {}>'.format(self.time)
