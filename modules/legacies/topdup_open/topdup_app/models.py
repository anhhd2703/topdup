from datetime import datetime
from typing import List
import db
import json
import re
from . import _config


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String, default='')
    publish_time = db.Column(db.String)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(512), nullable=False)
    similar_post_info = db.Column(db.String, default=json.dumps([]))
    max_score = db.Column(db.Float, default=0.0)
    embedd_vector = None  # not saved in database
    similar_post: List[object] = []  # similar post full information
    score = 0  # similarity score for each post
    domain = ''  # domain

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.url}', \
        '{self.similar_post_info}', '{self.domain}')"

    def similar_post_to_json(self):
        """
        Read similar_post_info in string format
        """
        return json.loads(self.similar_post_info)

    def get_similar_post_info(self):
        similar_post = self.similar_post_to_json()
        self.similar_post = []
        for i, p in enumerate(similar_post):
            selected_similar_post = self.query.get_or_404(p['id'])
            selected_similar_post.score = similar_post[i]['score']
            if selected_similar_post.url:
                selected_similar_post.domain = re.search(_config.split, selected_similar_post.url).group(1)
            if self.url:
                self.domain = re.search(_config.split, self.url).group(1)
            self.similar_post.append(selected_similar_post)
