from flask import Flask, render_template, session, redirect, request
import model
import jinja2
 
app = Flask(__name__) 
app.secret_key = ')V\xaf\xdb\x9e\xf7k\xccm\x1f\xec\x13\x7fc\xc5\xfe\xb0\x1dc\xf9\xcfz\x92\xe8'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route('/')
def index():
    user_list = model.session.query(model.User).limit(5).all()
    print "Here's the user_list %r" % user_list
    return render_template("user_list.html", users=user_list)

@app.route('/signup', methods = ['GET', 'POST'])
def user_signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        return signup_user()

def signup_user():
    user_email = request.form['email']
    user_password = request.form['password']

    if "login" in session:
        session["login"][user_email] = user_password 
    else:
        session["login"] = {user_email: user_password}
 
    return redirect("/")
 

@app.route('/login', methods=['GET', 'POST'])
def show_login():
    if request.method == "GET":
        return render_template("login.html")

    else: 
        return login_user()

def login_user():
    # We should be able to create a new user (signup)
    # We should be able to log in as a user
    #check DB - if they are in DB, they can log in, if they are no in DB, then sign up -or login failed   
    # use hashing here -- different than hashing or hashmap, use MD5 or SHA1 to store the password in the session
    #before you evaluate password, hash it  
    #check database to see if this user record matches what you have in DB
    #use salting too
    
    user_email = request.form['email']
    user_password = request.form['password']
 
    verify_user = model.session.query(model.User).filter_by(email = user_email).all()

    #the line below checks to see if a user is already in DB -if not, it sends them to signup page
    #if they are in DB, it checks to see if they're in session -if not, it adds them
    if verify_user == []:
        # print "You do not have a valid login. Check your email and password."
        return redirect("/signup")

    else: 
        if "login" in session:
            if user_email in session["login"]:
                session["login"][user_email] = user_password #reassigning as placeholder
            else:
                session["login"][user_email] = user_password 
        else:
            session["login"] = {user_email: user_password}
 
        return redirect("/")
            



# We should be able to view a list of all users
# We should be able to click on a user and view the list of movies they've rated, as well as the ratings
# We should be able to, when logged in and viewing a record for a movie, either add or update a personal rating for that movie.


if __name__ == "__main__":
    app.debug = True
    app.run()
