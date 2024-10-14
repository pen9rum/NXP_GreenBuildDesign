import React from 'react';
import livingroomIcon from '../assets/livingroom.png';
import bathroomIcon from '../assets/bathroom.png';
import bedroomIcon from '../assets/bedroom.png';
import kitchenIcon from '../assets/kitchen.png';

const InfoForm = ({ designInfo }) => {
  const { designName, length, width, rooms, windows } = designInfo;

  const roomIcons = {
    livingRoom: livingroomIcon,
    bathroom: bathroomIcon,
    bedroom: bedroomIcon,
    kitchen: kitchenIcon
  };

  return (
    <div className="p-4 rounded" style={{ backgroundColor: '#F0F0F0' }}>
      <h3 className="mb-4">Design Name: {designName}</h3>
      
      <div className="mb-3">
        <strong>House Area:</strong> {length}m × {width}m
      </div>

      <div className="mb-3">
        <strong>Room Amount:</strong>
        <div className="d-flex justify-content-between" style={{ maxWidth: '600px' }}>
          {Object.entries(rooms).map(([room, count]) => (
            <div key={room} className="text-center" style={{
              width: '120px',
              height: '120px',
              border: '1px solid black',
              borderRadius: '10px',
              padding: '10px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <img src={roomIcons[room]} alt={room} style={{ width: '40px', height: '40px', marginBottom: '5px' }} />
              <div style={{ fontSize: '0.8rem' }}>{room.replace(/([A-Z])/g, ' $1').trim()}</div>
              <div>{count}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-3">
        <strong>Windows:</strong>
        <ul>
          {Object.entries(windows).filter(([_, isPresent]) => isPresent).map(([position]) => (
            <li key={position}>{position}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default InfoForm;