from utils import db
from sqlalchemy import inspect

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    user_id = db.Column(db.String)
    is_inhouse_posting = db.Column(db.Boolean)
    status = db.Column(db.String(256))
    resume = db.Column(db.String(256))

    inhouse = db.relationship("Inhouse", backref="applications", lazy=True)
    external = db.relationship("External", backref="applications", lazy=True)
    interviewquestions = db.relationship("InterviewQuestion", backref="applications", lazy=True)
    def __repr__(self):
        return '<Application %r>' % self.id
    
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Inhouse(db.Model):
    __tablename__ = "inhouse"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    job_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Inhouse Application %r>' % self.id
    
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class External(db.Model):
    __tablename__ = "external"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    url = db.Column(db.String(256))
    position = db.Column(db.String(256))
    company = db.Column(db.String(256))
    date_posted = db.Column(db.String(256))
    deadline = db.Column(db.String(256))

    def __repr__(self):
        return '<External Application %r>' % self.id

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class InterviewQuestion(db.Model):
    __tablename__ = "interviewquestions"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    question = db.Column(db.String(256))

    def __repr__(self):
        return '<Interview Question %r' % self.Question

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
