import sqlalchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from .follow import followers
from .like import user_post


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    posts = relationship("Post", backref="users")
    liked = relationship('Post', secondary=user_post,
                         back_populates='liker', )

    followed = relationship('User',
                            secondary=followers,
                            primaryjoin=(followers.c.follower_id == id),
                            secondaryjoin=(followers.c.followed_id == id),
                            backref=backref('followers', lazy='dynamic'),
                            lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def liked_post(self, post):
        if not self.is_liked(post):
            self.liked.append(post)

    def unliked_post(self, post):
        if self.is_liked(post):
            self.liked.remove(post)

    def is_liked(self, post):
        return post in self.liked

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
