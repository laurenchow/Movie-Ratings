from flask import Flask, render_template, session, redirect, request
import model
import jinja2
 
 

app = Flask(__name__) 
app.secret_key = ')V\xaf\xdb\x9e\xf7k\xccm\x1f\xec\x13\x7fc\xc5\xfe\xb0\x1dc\xf9\xcfz\x92\xe8'
app.jinja_env.undefined = jinja2.StrictUndefined



@app.route('/')
def index():

    return "Welcome to my flashy movie ratings app. Would you like to log in?"

    # user_list = model.session.query(model.User).limit(5).all()
    # return render_template("user_list.html", users=user_list)




@app.route('/signup', methods = ['GET', 'POST'])
def user_signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        return signup_user()

def signup_user():
    user_email = request.form['email']
    user_password = request.form['password']
    current_user = model.session.query(model.User).filter_by(email = user_email).first()
    current_user_id = current_user.id


    if "login" in session: #this adds users to session
        session["login"][current_user_id] = user_email
    else:
        session["login"] = {current_user_id: user_email}

    print session
 
    new_user = model.User(email = user_email, password = user_password)
    model.session.add(new_user)
    model.session.commit() 
 
    return redirect("/")
 



@app.route('/login', methods=['GET', 'POST'])
def show_login():
    if request.method == "GET":
        return render_template("login.html")
    else: 
        return login_user()

def login_user():

    
    user_email = request.form['email']
    user_password = request.form['password']
 
    verify_user = model.session.query(model.User).filter_by(email = user_email).all()

    #the line below checks to see if a user is already in DB -if not, it sends them to signup page
    #if they are in DB, it checks to see if they're in session -if not, it adds them
    if verify_user == []:
        return redirect("/signup")
        # fix this to have user ID instead of email/pw
    else: 
        if "login" in session:
            session["login"][user_email] = user_password 
        else:
            session["login"] = {user_email: user_password}
 
        print session
        return redirect("/")
            
@app.route('/logout')
def logout_user():
    pass

@app.route('/viewallusers')
def view_all_users(): 
    user_list = model.session.query(model.User).limit(50).all()
    return render_template("user_list.html", users=user_list)



@app.route('/user/<int:id>')
def view_single_user(id):
    single_user = model.session.query(model.Rating).filter_by(user_id = id).all()
    return render_template("user.html", user = single_user)



@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def view_single_movie(id):
    # single_movie = model.session.query(model.Movie).filter_by(id = id).all()
    single_movie = model.session.query(model.Movie).get(id)
    print single_movie.ratings

    return render_template("movie.html", film = single_movie)



@app.route('/add_rating', methods=['GET', 'POST'])
def show_rating():
    if request.method == "GET":
        return render_template("add_rating.html")
    else:
        return add_your_own_rating()

def add_your_own_rating():
    my_own_rating = request.form['my_rating']


    print "Here's the rating %r" % my_own_rating
    print "Here's what is in session %r" % session["login"].keys()
    current_user_email = session["login"].keys() 
    #add in a log out function this way you can clear session and only have one 
    #store user ID in session too as USER id
    #key: login, value is user ID
    #will this work if you have multiple users in session? how to figure out which one is logged in?
    current_user_email = current_user_email[0].rstrip()    
    print "Here's the stripped user email %r" % current_user_email
    current_user = model.session.query(model.User).filter_by(email = current_user_email).one()
    print "Here's what is stored as current user %r" % current_user
    print "User ID %r" % current_user.id
    # print "Here's the user ID %r" % model.session.query(model.User).get(current_user) 
    return "add rating function working"

    # new_rating = model.Rating(current_user)
    # model.session.add(new_rating)
    # model.session.commit() 
 


    
if __name__ == "__main__":
    app.debug = True
    app.run()

    #check DB - if they are in DB, they can log in, if they are no in DB, then sign up -or login failed   
    # use hashing here -- different than hashing or hashmap, use MD5 or SHA1 to store the password in the session
    #check database to see if this user record matches what you have in DB