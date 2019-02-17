from utils import db
from sqlalchemy import inspect

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    user_id = db.Column(db.Integer)
    is_inhouse_posting = db.Column(db.Boolean)
    season = db.Column(db.String(256), db.ForeignKey('seasons.name'))
    status = db.Column(db.String(256))

    inhouse = db.relationship("Inhouse", backref="applications", lazy=True)
    external = db.relationship("External", backref="applications", lazy=True)
    def __repr__(self):
        return '<Application %r>' % self.id
    
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Inhouse(db.Model):
    __tablename__ = "inhouse"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    job_id = db.Column(db.Integer)
    resume = db.Column(db.String(256))
    comments = db.Column(db.String(256))

    def __repr__(self):
        return '<Inhouse Application %r>' % self.id

class External(db.Model):
    __tablename__ = "external"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    job_url = db.Column(db.String(256))
    job_title = db.Column(db.String(256))

    def __repr__(self):
        return '<External Application %r>' % self.id

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Season(db.Model):
    __tablename__ = "seasons"
    name = db.Column(db.String, primary_key=True)
    
    application = db.relationship("Application", backref="seasons", lazy=True)

    def __repr__(self):
        return '<Season %r>' % self.name

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
