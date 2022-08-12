import sqlalchemy
from data.db_session import SqlAlchemyBase

followers = sqlalchemy.Table('followers', SqlAlchemyBase.metadata,
                             sqlalchemy.Column('follower_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('users.id')),
                             sqlalchemy.Column('followed_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('users.id'))
                             )
