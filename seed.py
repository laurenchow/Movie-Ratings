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
        session.commit()
            # print ' '.join(row)

    print user_table 

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as csvfile:
        item_table= csv.reader(csvfile, delimiter='|')
        for row in item_table:
            new_item= model.Movie(id = row[0], name=row[1], released_at= row[2], imdb_url=row[3])
            session.add(new_item)
        session.commit()

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)




if __name__ == "__main__":
    s= model.connect()
    main(s)
