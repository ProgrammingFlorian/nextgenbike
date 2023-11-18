from datetime import datetime

from webapp.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    trips = db.relationship('Trip', backref='rider', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end = db.Column(db.DateTime)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    sensors = db.relationship('Sensors', backref='trip', lazy='dynamic')

    def __repr__(self):
        return '<Trip {}>'.format(self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Sensors(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), primary_key=True)

    vibration = db.Column(db.Integer)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    acceleration_x = db.Column(db.Float)
    acceleration_y = db.Column(db.Float)
    acceleration_z = db.Column(db.Float)
    gyroscope_x = db.Column(db.Float)
    gyroscope_y = db.Column(db.Float)
    gyroscope_z = db.Column(db.Float)

    crash = db.Column(db.Integer, nullable=True)
    terrain = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Sensor data at {self.time} on trip {self.trip_id}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Terrain(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), primary_key=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    terrain = db.Column(db.Integer)

    def __repr__(self):
        return f"Terrain from {self.time} on trip {self.trip_id}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
