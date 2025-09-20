import React from 'react';
import './SongCard.css';

function SongCard({ song, image, isSelected, onClick }) {
    return (
        <div className={`song-card ${isSelected ? 'selected' : ''}`} onClick={onClick}>
            <img src={image} alt={song.genre} className="genre-image" />
            <div className="card-content">
                <h3 className="song-title">{song.title}</h3>
                <p className="song-artist">Artist: {song.artist}</p>
                <p className="song-genre">Genre: {song.genre}</p>
            </div>
        </div>
    );
}

export default SongCard;
