import React, { useState } from 'react';
import "../css/AirbnbRecommendation.css";

const AirbnbRecommendation = () => {
  const [selectedNeighborhood, setSelectedNeighborhood] = useState('');
  const [selectedRoomType, setSelectedRoomType] = useState('');
  const [minimumNights, setMinimumNights] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');

  const neighborhoods = ['bronx', 'brooklyn', 'manhattan', 'queens','staten island'];
  const roomType = ['entire home/apt', 'private room', 'shared room']

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!/^\d+$/.test(minimumNights) || minimumNights < 1 || minimumNights > 74) {
      setError('Minimum Nights should be a number between 1 and 74.');
      return;
    } else {
      setError('');
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/hotelRecommendations?grp=${selectedNeighborhood}&room=${selectedRoomType}&nights=${minimumNights}`);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setRecommendations(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  return (
    <div>
      <h1>Airbnb Recommendation App</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Neighborhood:
          <select value={selectedNeighborhood} onChange={(e) => setSelectedNeighborhood(e.target.value)}>
            <option value="">Select a neighborhood</option>
            {neighborhoods.map((neighborhood) => (
              <option key={neighborhood} value={neighborhood}>
                {neighborhood}
              </option>
            ))}
          </select>
        </label>
        <br />
        <label>
          Room Type:
          <select value={selectedRoomType} onChange={(e) => setSelectedRoomType(e.target.value)}>
            <option value="">Select a roomtype</option>
            {roomType.map((roomType) => (
              <option key={roomType} value={roomType}>
                {roomType}
              </option>
            ))}
          </select>
        </label>
        <br />
        <label>
          Number of Nights:
          <input type="number" value={minimumNights} onChange={(e) => setMinimumNights(e.target.value)} />
        </label>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <br />
        <button type="submit" disabled={!selectedNeighborhood}>Get Recommendations</button>
      </form>

      <h2>Recommendations:</h2>
      <ul>
      {recommendations.estimated_price && recommendations.estimated_price.length > 0 ? (
        <ul>
          {recommendations.estimated_price.map((price, index) => (
            <li key={index}>
              <strong>Property Name:</strong> {recommendations.name[index]}<br />
              <strong>Host Name:</strong> {recommendations.host_name[index]}<br />
              <strong>Neighbourhood:</strong> {recommendations.neighbourhood[index]}<br />
              <strong>Room Type:</strong> {recommendations.room_type[index]}<br />
              <strong>Estimated Price:</strong> {price}<br />
            </li>
          ))}
        </ul>
      ) : (
        <p>No recommendations available.</p>
      )}
      </ul>
    </div>
  );
};

export default AirbnbRecommendation;