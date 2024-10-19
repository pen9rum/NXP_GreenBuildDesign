import React, { useState } from 'react';
import { Carousel } from 'react-bootstrap';
import livingroomIcon from '../assets/livingroom.png';
import bathroomIcon from '../assets/bathroom.png';
import bedroomIcon from '../assets/bedroom.png';
import kitchenIcon from '../assets/kitchen.png';

const InfoForm = ({ designInfo }) => {
  const { designName, length, width, rooms, windows, gpt_configurations } = designInfo;
  const [currentIndex, setCurrentIndex] = useState(0);

  const roomIcons = {
    livingRoom: livingroomIcon,
    bathroom: bathroomIcon,
    bedroom: bedroomIcon,
    kitchen: kitchenIcon
  };

  const handleSelect = (selectedIndex) => {
    setCurrentIndex(selectedIndex);
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

      {gpt_configurations.configurations && gpt_configurations.configurations.length > 0 && (
        <div className="mt-4">
          <h4>Configuration Options:</h4>
          <Carousel activeIndex={currentIndex} onSelect={handleSelect}>
            {gpt_configurations.configurations.map((config, index) => (
              <Carousel.Item key={index}>
                <img
                  className="d-block w-100"
                  src={`data:image/png;base64,${config.image}`}
                  alt={`Configuration ${index + 1}`}
                />
                <Carousel.Caption>
                  <h5>{config.name}</h5>
                </Carousel.Caption>
              </Carousel.Item>
            ))}
          </Carousel>
          
          <div className="mt-3">
            <h5>{gpt_configurations.configurations[currentIndex].name}</h5>
            <p>{gpt_configurations.configurations[currentIndex].description}</p>
            <h6>Energy Efficiency Report:</h6>
            <p>Grade: {gpt_configurations.configurations[currentIndex].energy_efficiency_report.energy_efficiency_grade}</p>
            <p>Total Score: {gpt_configurations.configurations[currentIndex].energy_efficiency_report.total_score}</p>
            <h6>Detailed Scores:</h6>
            <ul>
              {Object.entries(gpt_configurations.configurations[currentIndex].energy_efficiency_report.detailed_scores).map(([key, value]) => (
                <li key={key}>{key.replace(/_/g, ' ')}: {value}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default InfoForm;