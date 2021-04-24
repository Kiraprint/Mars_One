import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    city_from = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.Date)

    jobs = orm.relation("Jobs", secondary="users_to_jobs", backref="users")
    departments = orm.relation("Department", secondary="users_to_departments", backref="users")

    def __repr__(self):
        return f'<Colonist> {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
