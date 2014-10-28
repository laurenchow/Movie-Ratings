from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE= None
Session= None
Base = declarative_base()

### Class declarations go here
class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=True)
    password =  Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode =  Column(String(15), nullable= True) 


class Movie(Base):
    __tablename__="movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    released_at = Column(Integer, nullable= True)
    imdb_url = Column(String(56), nullable = True)


class Rating(Base):
    __tablename__="ratings"

    id = Column(Integer, primary_key= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id= Column(Integer, ForeignKey('movies.id'))
    rating = Column(Integer, nullable=True) 

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=rating))
# how can you search using sql in python  without running sqlite3? can you?
def connect():
    global ENGINE
    global Session

    # ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    # Session = sessionmaker(bind=ENGINE)

    # return Session()


### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
