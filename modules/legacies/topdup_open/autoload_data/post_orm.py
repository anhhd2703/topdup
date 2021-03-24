import os
import pickle
import json
import datetime
import sqlalchemy
import pandas as pd
from glob import glob
from random import randint, shuffle, choice, choices
from sqlalchemy import create_engine
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .log import get_logger
from ._config import DATABASE_URI


logger = get_logger(__name__)
engine = create_engine(DATABASE_URI, echo=False)
Base = declarative_base()

class Post(Base):
    """ORM class to communicate with database"""
    
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    author = Column(String, default='')
    publish_time = Column(String, default='')
    updated_time = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String)
    max_score = Column(Float, default=0.0)

    # similar_post_info: save all post_id and score that nearest the post,
    # format: [{id:, score:},..], save in database with String type
    similar_post_info = Column(String, default=json.dumps([]))
    embedd_vector = None # not saved in database

    def set_similar_post_info(self, similar_info):
        """
        Set similar_post_info value and dump to string to save in database
        input: [{id:, score:}, {id: , score:}]
        """
        if len(similar_info) == 0:
            return False
        similar_info = sorted(
            similar_info, key=lambda x: x['score'], reverse=True)
        self.similar_post_info = json.dumps(similar_info)
        self.max_score = round(similar_info[0]['score'], 3)
        return True

    def add_similar_info(self, post_info):
        """
        Add a post_info to similar_post_info and save in database
        Input format: {id:, score:}
        """
        json_info = json.loads(self.similar_post_info)
        for item in json_info:
            if item['url'] == post_info['url']:
               return None

        json_info.append(post_info)
        json_info = sorted(json_info, key=lambda x: x['score'], reverse=True)
        self.max_score = round(json_info[0]['score'], 3)
        self.similar_post_info = json.dumps(json_info)

    def get_similar_post_info(self):
        """
        Read similar_post_info in string format
        """
        json_info = json.loads(self.similar_post_info)
        return json_info

    def __repr__(self):
        return f" id: {self.id} \n title: {self.title}  \n\n"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_session():
    """Init session for ORM classes"""
    session = Session()
    return session


def load_pickle_data(fn):
    all_data = []
    if os.path.isfile(fn):
        try:
            f = open(fn, 'rb+')
            all_data = pickle.load(f)
            f.close()
        except:
            logger.exception("pickle file is empty")
    return all_data


def check_valid_post(post, session):
    try:
        l = len(post.content)
        if l < MIN_CHARACTER_LEN:
            logger.debug(f'post content is too short: length {l}, {post.title},  {post.url}')
            return False

        all_post = session.query(Post.title, Post.url).all()
        for title, url in all_post:
            if post.title == title and post.url == url:
                logger.debug(f'This post is already exists in database: {post.title}')
                return False
        return True

    except Exception as e:
        logger.exception(e)
        return False

df = None

def fake_data():
    global df
    if df is None:
        df = pd.read_csv(FAKE_DATASET)
    id = randint(0, len(df)-1)
    item = df.loc[id]
    
    try:
        url = item['link']
    except:
        url = ''
    post = Post(
        title=item['title'],
        content=item['content'],
        url=url,
    )
    return post
