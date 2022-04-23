import sqlalchemy
from data.db_session import SqlAlchemyBase

user_like = sqlalchemy.Table('likes', SqlAlchemyBase.metadata,
                             sqlalchemy.Column('liked_id', sqlalchemy.Integer,
                                                        sqlalchemy.ForeignKey("posts_user.id")),
                             sqlalchemy.Column('liker_id', sqlalchemy.Integer,
                                                        sqlalchemy.ForeignKey("users.id")))