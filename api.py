# this imports the nesscary classes from the flask library
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

#this creates an instance of the Flask application
app = Flask(__name__)
# I am using SQLAlchemy to set up the database using sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# model for the database so that the database knows the shape of the data that I will be storing

class SongModel(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    artist = db.Column(db.String(80), unique=False, nullable=False)
    # what to return when the class is used
    def __ref__(self):
        return f"Song(title = self.title, artist = self.artist)"

#this tells Flask to execute the hello world function whenever the user visiting the root URL of the api
@app.route('/')

def hello_world():
    # instead of simply returning a string this ensures that the response is in JSON format
    return jsonify(
        {'message': 'Hello, World!'}
    )
# this is the standard entry point for running a Python script. the debug=True is a development flag that automatically reloads the server when I make code changes
if __name__=='__main__':
    app.run(debug=True)
