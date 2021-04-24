import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    association_table = sqlalchemy.Table(
        'users_to_departments',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('user', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('users.id')),
        sqlalchemy.Column('department', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('departments.id'))
    )
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)

    creator = orm.relation('User')
