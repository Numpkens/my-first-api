# my-first-api

## The Purpose

The purpose of this project was to take concepts that learned in Scrimba's FullStack path specifically the React modules and combine them with the BackEnd concepts I am learning on boot.dev and create a React application that consumes data from an API that I build using Python with Flask. It allows users to retrieve songs and artists from the database and add artists and songs to the database and create thier own custom playlist.

### Setting Up The API

1. I started by ensuring that I had all the proper dependencies imported.

```Python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_cors import CORS
```
2. I then created an instance of the Flask application. However, later when I was implementing the React frontend I found that I was running into cors issues keeping the application from displaying propperly. So, I added the CORS import and added it to the instance. I also used SQLAlchemy to set up the database using SQLite.

```Python
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)
```

3. Next, I made a class for the song model in order for the database to know the shape of the data that will be stored. As well as adding help text in case the user doesn't put the data into the form as expected. 

```Python
class SongModel(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    artist = db.Column(db.String(80), unique=False, nullable=False)
    genre = db.Column(db.String(80), unique=False, nullable=False)
    # what to return when the class is used
    def __repr__(self):
        return f"Song(title = {self.title}, artist = {self.artist}, genre = {self.genre})"

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
```

4.  Then, I created a class that gave the user the ability to run a get operation as well as a put operation on the api. At the same time gave users endpoints in which to access the data. Also, added an error code for a bad return. 
```Python
class Songs(Resource): 
    @marshal_with(songFields)
    def get(self):
        songs = SongModel.query.all()
        return songs
    
    @marshal_with(songFields)
    def post(self):
        args = song_args.parse_args()
        song = SongModel(title=args['title'], artist=args['artist'], genre=args['genre'])
        db.session.add(song)
        db.session.commit()
        return song, 201
api.add_resource(Songs, '/api/songs/')
```

### React FrontEnd

The front end is built with React. The App.js file is the main component of the application. It handles the user interface and logic for the application.

1. I used React hooks like useState and useEffect to manage the application's state, such as the list of songs, loading status, and UI elements like the add song form or playlist view.

```JSX
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedSongs, setSelectedSongs] = useState([]);
  const [showPlaylist, setShowPlaylist] = useState(false);

```

2. I defined an asynchronous function fetchData that uses the fetch API to make a GET request to the Flask API's /api/songs/ endpoint (http://127.0.0.1:5000/api/songs/).

```JSX 
 const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/songs/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };
```

3. Used the useEffect hook to call fetchData when the component mounts, ensuring the song data is loaded when the application starts.
```JSX
useEffect(() => {
    fetchData();
  }, []);

  const handleAddSong = () => {
    setShowAddForm(true);
    setShowPlaylist(false);
  };

  const handleSongAdded = () => {
    setShowAddForm(false);
    fetchData();
  };

  const handleGeneratePlaylist = () => {
    setShowPlaylist(true);
  };

  const handleBackToAllSongs = () => {
    setShowPlaylist(false);
    setSelectedSongs([]);
  };
```

4. Conditionally renderd different UI elements, such as a list of SongCard components or an AddSongForm, based on the application's state.

```JSX
 const handleCardClick = (songId) => {
    setSelectedSongs((prevSelected) => {
      if (prevSelected.includes(songId)) {
        return prevSelected.filter((id) => id !== songId);
      } else {
        return [...prevSelected, songId];
      }
    });
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }
```

5. Made the SongCard component display the song's information (title, artist, genre) and an image based on the genre.
```JSX
div className="song-cards-container">
        {showPlaylist ? (
          data
            .filter((song) => selectedSongs.includes(song.id))
            .map((song) => (
              <SongCard
                key={song.id}
                song={song}
                image={genreImages[song.genre.toLowerCase()]}
              />
            ))
        ) : (
          data.length > 0 ? (
            data.map((song) => (
              <SongCard
                key={song.id}
                song={song}
                image={genreImages[song.genre.toLowerCase()]}
                isSelected={selectedSongs.includes(song.id)}
                onClick={() => handleCardClick(song.id)}
              />
            ))
          ) : (
            <p>No songs found. Add one!</p>
          )
        )}
```
6. Ensures that the application also handles user interactions, such as adding a new song, generating a playlist, and navigating between views.

In summary, the React front end serves as the user interface, fetching and displaying data from the Python/Flask API, which serves as the backend data source and handles all the data logic.


## Conclusion

I learned alot from building this project. And was pariculrly proud of the api. 
