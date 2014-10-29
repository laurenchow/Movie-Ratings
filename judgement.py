from flask import Flask, render_template, session, redirect, request
import model
import jinja2
 
 

app = Flask(__name__) 
app.secret_key = ')V\xaf\xdb\x9e\xf7k\xccm\x1f\xec\x13\x7fc\xc5\xfe\xb0\x1dc\xf9\xcfz\x92\xe8'
app.jinja_env.undefined = jinja2.StrictUndefined



@app.route('/')
def index():
    user_list = model.session.query(model.User).limit(5).all()
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
    user_age = request.form ['age']
    user_zipcode = request.form ['zipcode']
    if "login" in session: #this adds users to session
        session["login"][user_email] = user_password 
    else:
        session["login"] = {user_email: user_password}
 
    new_user = model.User(email = user_email, password = user_password, age=user_age, zipcode=user_zipcode)
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
    #check DB - if they are in DB, they can log in, if they are no in DB, then sign up -or login failed   
    # use hashing here -- different than hashing or hashmap, use MD5 or SHA1 to store the password in the session
    #before you evaluate password, hash it (use salting too)
    #check database to see if this user record matches what you have in DB

    
    user_email = request.form['email']
    user_password = request.form['password']
 
    verify_user = model.session.query(model.User).filter_by(email = user_email).all()

    #the line below checks to see if a user is already in DB -if not, it sends them to signup page
    #if they are in DB, it checks to see if they're in session -if not, it adds them
    if verify_user == []:
        return redirect("/signup")

    else: 
        if "login" in session:
            session["login"][user_email] = user_password 
        else:
            session["login"] = {user_email: user_password}
 
        print session
        return redirect("/")
            
@app.route('/viewallusers')
def view_all_users(): 
    user_list = model.session.query(model.User).limit(50).all()
    return render_template("user_list.html", users=user_list)

# we need to figure out how we pass a single user to this
@app.route('/user')
def view_single_user():
    return render_template("user.html")

# We should be able to view a list of all users
# We should be able to click on a user and view the list of movies they've rated, as well as the ratings
# We should be able to, when logged in and viewing a record for a movie, either add or update a personal rating for that movie.

@app.route('movie')
def view_single_movie():
    return render_template("movie.html")
if __name__ == "__main__":
    app.debug = True
    app.run()
