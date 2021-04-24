import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    association_table = sqlalchemy.Table(
        'users_to_jobs',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('user', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('users.id')),
        sqlalchemy.Column('job', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('jobs.id'))
    )


    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.Date)
    end_date = sqlalchemy.Column(sqlalchemy.Date)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)

    categories = orm.relation("Categories", secondary="categories_to_jobs", backref='jobs')
    creator = orm.relation('User')

    def __repr__(self):
        return f'<Job> {self.job}'
