import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from .like import user_post


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    miniature = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    autor_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("users.id"))
    autor = orm.relation('User', back_populates='posts')

    liker = relationship(
        'User',
        secondary=user_post,
        back_populates="liked",
    )