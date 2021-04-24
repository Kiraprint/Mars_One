import sqlalchemy
from data.db_session import SqlAlchemyBase


class Categories(SqlAlchemyBase):
    association_table = sqlalchemy.Table(
        'categories_to_jobs',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('category', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('category.id')),
        sqlalchemy.Column('job', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('jobs.id')))
    __tablename__ = 'category'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return str(self.id)
