import sqlalchemy
from data.db_session import SqlAlchemyBase

user_post = sqlalchemy.Table('likes', SqlAlchemyBase.metadata,
                             sqlalchemy.Column('liked_id', sqlalchemy.Integer,
                                                        sqlalchemy.ForeignKey("posts.id")),    #id поста, который лайкнули
                             sqlalchemy.Column('liker_id', sqlalchemy.Integer,
                                                        sqlalchemy.ForeignKey("users.id")))    #id юзера, который лайкнул пост