# this imports the nesscary classes from the flask library
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

#this creates an instance of the Flask application
app = Flask(__name__)
# I am using SQLAlchemy to set up the database using sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# model for the database so that the database knows the shape of the data that I will be storing

class SongModel(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    artist = db.Column(db.String(80), unique=False, nullable=False)
    genre = db.Column(db.String(80), unique=False, nullable=False)
    # what to return when the class is used
    def __ref__(self):
        return f"Song(title = self.title, artist = self.artist, genre = self.genre)"

song_args = reqparse.RequestParser()

song_args.add_argument('title', type=str, required=True, help="Title can not be blank")
song_args.add_argument('artist', type=str, required=True, help="Artist name can not be blank")
song_args.add_argument('genre', type=str, required=True, help="Genre can not be blank")
# add fields for the json data
songFields = {
    'id':fields.Integer,
    'title':fields.String,
    'artist':fields.String,
    'genre':fields.String,
}

# create a get method for users to be able to request data from end point
class Songs(Resource):
    @marshal_with(songFields)
    def get(self):
        songs = SongModel.query.all()
        return songs
    @marshal_with(songFields)
    #allow users to add songs to the database
    def post(self):
        args = song_args.parse_args()
        song = SongModel(title=args['title'], artist=args['artist'], genre=args['genre'])
        db.session.add(song)
        db.session.commit()
        songs = SongModel.query.all()
        return songs, 201

# create the end point for users to receive the data
api.add_resource(Songs, '/api/songs/')

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
