from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from hidden import jason_db_connect, josh_db_connect, shhh

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://food4you:food4you@localhost:8889/food4you"

# Comment out other devs' db's to run the app locally
#app.config['SQLALCHEMY_DATABASE_URI'] = jason_db_connect
#app.config['SQLALCHEMY_DATABASE_URI'] = josh_db_connect


app.secret_key = 'shhh,dont_tellanyone44329'

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)
