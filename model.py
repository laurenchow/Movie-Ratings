from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

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
    user_id = Column(Integer, nullable=True)
    movie_id= Column(Integer, nullable=True)
    rating = Column(Integer, nullable=True) 
    
# how can you search using sql in python  without running sqlite3? can you?
def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
