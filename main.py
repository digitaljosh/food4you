from flask import request, redirect, render_template, session, flash
import sqlalchemy
import requests

from app import app, db
from models import User
from hashutils import check_pw_hash


# Require login to access specific endpoints
@app.before_request
def login_required():
    ''' makes sure user logged in to display page '''
    not_allowed_routes = [''' [enter route funtion name, example: 'index'] ''',]
    if request.endpoint in not_allowed_routes and 'username' not in session:
        flash("You need to be logged in first!", 'negative')
        return redirect('/')

# Landing page
@app.route("/")
def index():
    return render_template('home.html')


# React example page
@app.route("/react")
def react_example():
    return render_template('react-test.html')


# Sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        
        # Get form data
        name = request.form['username']
        email = request.form['email']
        p_word = request.form['passw']
        con_pword = request.form['conf_pass']

        # if user credentials already exist, store in variable
        user_with_same_name = User.query.filter_by(username=name).count()

        # Sign up validation
        if user_with_same_name > 0:
            flash("Someone is already using that name", 'negative')
            return render_template('signup.html')
        elif len(p_word) < 6 or len(p_word) > 20:
            flash("Passwords must be at least 6 chars long, 20 at most.", "negative")
            return render_template('signup.html', username=name)
        elif p_word != con_pword:
            flash("Passwords don't match!", 'negative')
            return render_template('signup.html', username=name, email=email)

        else:
            # everything entered correctly we instantiate instance of new User class 
            new_user = User(name, p_word, email)
           
            # commit to database
            db.session.add(new_user)
            db.session.commit()

            # create anything else associated with user, example: cookbook
            '''new_cookbook = Cookbook(owner_id=new_user.id)
            db.session.add(new_cookbook)
            db.session.commit()'''

            # set current session
            session['username'] = new_user.username
            
            return render_template('full-calendar.html', user=User.getUserByName(session['username']))


@app.route('/login', methods=['GET', 'POST'])
def login():

    # requesting access to login page
    if request.method == 'GET':
        # Error handling: try and except 
        try:
            # auto login if user is in session
            if session['username']:
                name = session['username']
                recipes = User.getListUserRecipes(name)
                return render_template('full-calendar.html', user=User.getUserByName(name), recipes=recipes)
        # if errors occur, except block handles it
        except KeyError:
            return render_template('login.html')
        except AttributeError: # no one in db yet NoneType
            flash("This is your first rodeo", 'negative')
            return render_template('login.html')

    # if no user in session, send login credentials to server to login 
    elif request.method == 'POST':
        tried_name = request.form['username']
        tried_pw = request.form['password']
        user_to_check = User.query.filter_by(username=tried_name)

        # login validations
        if user_to_check.count() == 1:
            user = user_to_check.first()
            if user and check_pw_hash(tried_pw, user.pw_hash):
                session['username'] = user.username
                return redirect('/full-calendar')
            else:
                flash("Nice try!", 'negative')
                return redirect('/login')
        else:
            flash("Either you mistyped your username or you don't have an account.", 'negative')
            return render_template('login.html')


@app.route('/search', methods=['POST', 'GET'])
def search_function():

    if request.method == 'POST':

        # example method to query API
        search_query = request.form['search']
        search_query = search_query.replace(" ","+")
        
        api = "http://supermarketownbrandguide.co.uk/api/newfeed.php?json=search&q="
        append = "&page=0&apikey=3wwbjwb2i7v31yqd9ipx"
        url = api + search_query + append
        
        '''headers={
            "X-Mashape-Key": ,
            "Accept": "application/json"
            }'''

        # JSON data back from API
        json_data = requests.get(url).json()
        print(json_data)

        return render_template('search.html', template_variable=json_data)

    # GET request
    else: 
        return render_template('search.html')



@app.route('/logout')
def logout():
    try:
        if session['username']:
            del session['username']
            flash("See ya next time!", 'positive')
            return redirect("/")
    except KeyError:
        flash("You aren't currently logged in!", 'negative')
        return redirect("/")



if __name__ == '__main__':
    app.run()