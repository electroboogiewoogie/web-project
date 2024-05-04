from data import db_session
import sqlalchemy
import datetime
class User(db_session.SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.String)
    remember_form = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True, default=False)
    reviews_count = sqlalchemy.Column(sqlalchemy.Integer, )
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
class Reviews(db_session.SqlAlchemyBase):
    __tablename__ = 'films'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer)
    name_user = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mark = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    review = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String)


class Films(db_session.SqlAlchemyBase):
    __tablename__ = 'films_all'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    mark = sqlalchemy.Column(sqlalchemy.String)
    average_mark = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    genres = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.String)
    countReviews = sqlalchemy.Column(sqlalchemy.Integer)