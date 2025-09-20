import React, { useState, useEffect } from 'react';
import './App.css';
import SongCard from './components/SongCard.jsx';
import AddSongForm from './components/AddSongForm.jsx';

// Import local images directly
import popImage from './assets/pop.jpg';
import rockImage from './assets/rock.jpg';
import hiphopImage from './assets/hiphop.jpg';
import rnbImage from './assets/r&b.jpg';

// Map genres to imported image files
const genreImages = {
  'pop': popImage,
  'rock': rockImage,
  'hip-hop': hiphopImage,
  'r&b': rnbImage,
};

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedSongs, setSelectedSongs] = useState([]);
  const [showPlaylist, setShowPlaylist] = useState(false);

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

  return (
    <div className="App">
      <header className="App-header">
        {showPlaylist ? (
          <>
            <h2>Your Playlist</h2>
            <button onClick={handleBackToAllSongs}>Back to All Songs</button>
          </>
        ) : (
          <>
            <h1>My Song Collection</h1>
            <div className="button-container">
              <button onClick={handleAddSong}>Add Song</button>
              <button onClick={handleGeneratePlaylist}>Generate Playlist</button>
            </div>
          </>
        )}
      </header>

      {showAddForm && <AddSongForm onSongAdded={handleSongAdded} />}

      <div className="song-cards-container">
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
      </div>
    </div>
  );
}

export default App;
