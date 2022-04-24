import sqlalchemy
from data.db_session import SqlAlchemyBase

likers = sqlalchemy.Table('likers', SqlAlchemyBase.metadata,
                          sqlalchemy.Column('liker_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('posts_user.id')),
                          sqlalchemy.Column('liked_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('posts_user.id'))
)