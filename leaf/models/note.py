# -*- coding: utf-8 -*-

import datetime

from leaf.extentions import db

class NoteQuery:

    @classmethod
    # 如果网站2500年还在，请维护者记得修改该函数的默认参数end
    def get_notes_by_author(cls, user_id, begin=datetime.datetime(1900,1,1), end=datetime.datetime(2500,1,1)):
        # TODO:等日记写多了直接all()没有性能问题么？加个分页？
        return Note.query.filter(Note.user_id==user_id, Note.time>=begin, Note.time<=end).order_by('-id').all()

    @classmethod
    def get_notes_by_datenum(cls, user_id, datenum):
        return Note.query.filter(Note.user_id==user_id, Note.datenum==datenum).order_by('-id').all()

    @classmethod
    def get_datenum_by_user(cls, user_id):
        return db.session.query(Note.datenum).filter(Note.user_id==user_id).distinct()

    @classmethod
    def get_recent_note_by_user(cls, user_id):
        note = Note.query.filter_by(user_id=user_id).order_by('-id').first()
        return note

    @classmethod
    def get_older_note(cls, user_id, note_id):
        note = Note.query.filter(Note.user_id==user_id, Note.id<note_id).order_by('-id').first()
        return note

    @classmethod
    def get_newer_note(cls, user_id, note_id):
        note = Note.query.filter(Note.user_id==user_id, Note.id>note_id).order_by('id').first()
        return note


class Note(db.Model):
    query_obj = NoteQuery()
    __tablename__ = 'note'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, nullable=False, key='user_id')
    time = db.Column('time', db.TIMESTAMP, nullable=False)
    datenum = db.Column('datenum', db.Integer, nullable=False)
    content = db.Column('content', db.Text, nullable=False)

    def __init__(self, user_id, content, time):
        self.user_id = user_id
        self.time = time
        self.datenum = self.time.strftime('%Y%m')
        self.content = content

    def __repr__(self):
        return "<Note id=%s, author_id=%s>" % (self.id, self.user_id)

    @classmethod
    def create(cls, user_id, content, time=None):
        if not time:
            time = datetime.datetime.now()
        note = cls(user_id, content, time)
        db.session.add(note)
        db.session.commit()
        return note

    def update(self, content):
        self.content = content
        self.update_time = datetime.datetime.now()
        db.session.commit()

    @classmethod
    def gets_by_author(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
