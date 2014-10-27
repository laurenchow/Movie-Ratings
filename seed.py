import model
import csv

def load_users(session):
    with open('seed_data/u.user', 'rb') as csvfile:
        user_table = csv.reader(csvfile, delimiter='|')
        for row in user_table:
            # delete by hand or add in 
            # check and see if there's an ID in the database for the data:
            # if so, don't do anything, if not, add a row 
            #if id == "is null":
            new_user = model.User(id = row[0], age = row[1], zipcode = row[4]) 
            session.add(new_user)
        
            # print ' '.join(row)

    print user_table 

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as csvfile:
        item_table= csv.reader(csvfile, delimiter='|')
        for row in item_table:
            movie_title = row[1].split()
            for i, words in enumerate(movie_title):
                if words.isalpha() != True:
                    movie_title.pop(i)
                movie_string = ' '.join(movie_title)
                movie_string = movie_string.decode("latin-1")

            new_item= model.Movie(id = row[0], name=movie_string, released_at= row[2], imdb_url=row[4])
            session.add(new_item)
     
        print item_table

def load_ratings(session):
    with open('seed_data/u.data', 'rb') as csvfile:
        ratings_table = csv.reader(csvfile, delimiter='\t')
        for row in ratings_table:
            new_rating= model.Rating(user_id = row[0], movie_id = row[1], rating = row[2])
            session.add(new_rating)
        
       
        
def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

    session.commit()






if __name__ == "__main__":
    s = model.connect()
    main(s) 