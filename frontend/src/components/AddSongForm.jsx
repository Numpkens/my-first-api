import React, { useState } from 'react';
import './AddSongForm.css'; // We'll create this CSS file next

function AddSongForm({ onSongAdded }) {
  const [title, setTitle] = useState('');
  const [artist, setArtist] = useState('');
  const [genre, setGenre] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newSong = { title, artist, genre };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/songs/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSong),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Call the function passed from App.js to update the song list
      onSongAdded();

      // Clear the form
      setTitle('');
      setArtist('');
      setGenre('');
    } catch (e) {
      console.error('Failed to add song:', e);
    }
  };

  return (
    <form className="add-song-form" onSubmit={handleSubmit}>
      <input 
        type="text" 
        placeholder="Title" 
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <input 
        type="text" 
        placeholder="Artist" 
        value={artist}
        onChange={(e) => setArtist(e.target.value)}
        required
      />
      <input 
        type="text" 
        placeholder="Genre" 
        value={genre}
        onChange={(e) => setGenre(e.target.value)}
        required
      />
      <button type="submit">Add Song</button>
    </form>
  );
}

export default AddSongForm;
