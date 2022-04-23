import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class PostUser(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts_user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    autor_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("users.id"))
    autor = orm.relation('User', back_populates='posts_user')
