import React, { useState, useEffect } from 'react';
import CreatingDesignModal from './CreatingDesignModal';
import { Modal, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import bathroomIcon from '../assets/bathroom.png';
import bedroomIcon from '../assets/bedroom.png';
import kitchenIcon from '../assets/kitchen.png';
import livingroomIcon from '../assets/livingroom.png';
import designImage from '../assets/design.jpeg';
import directionImage from '../assets/Direction.png';
import loading from '../assets/Pic4.webp';

const DesignForm = ({ onSubmit, initialData, isDirty, setIsDirty }) => {
  const navigate = useNavigate();
  const [designName, setDesignName] = useState(initialData?.designName || '');
  const [length, setLength] = useState(initialData?.length || '');
  const [width, setWidth] = useState(initialData?.width || '');
  const [rooms, setRooms] = useState(initialData?.rooms || {
    livingRoom: 1,
    bathroom: 1,
    bedroom: 1,
    kitchen: 1
  });
  const [windows, setWindows] = useState(initialData?.windows || {
    top: false,
    right: false,
    bottom: false,
    left: false
  });
  const [showModal, setShowModal] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  useEffect(() => {
    if (initialData) {
      setDesignName(initialData.designName || '');
      setLength(initialData.length || '');
      setWidth(initialData.width || '');
      setRooms(initialData.rooms || {
        livingRoom: 1,
        bathroom: 1,
        bedroom: 1,
        kitchen: 1
      });
      setWindows(initialData.windows || {
        top: false,
        right: false,
        bottom: false,
        left: false
      });
    }
  }, [initialData]);

  useEffect(() => {
    const isFormDirty = designName !== '' || length !== '' || width !== '' ||
      Object.values(rooms).some(value => value !== 1) ||
      Object.values(windows).some(value => value === true);
    setIsDirty(isFormDirty);
  }, [designName, length, width, rooms, windows, setIsDirty]);


  const handleSubmit = (e) => {
    e.preventDefault();
    const designInfo = {
      designName,
      length,
      width,
      rooms,
      windows
    };
    onSubmit(designInfo);
    setShowModal(true);
    setIsDirty(false);
  };

  const handleNewDesign = () => {
    if (isDirty) {
      setShowConfirmModal(true);
    } else {
      resetForm();
    }
  };

  const resetForm = () => {
    setDesignName('');
    setLength('');
    setWidth('');
    setRooms({
      livingRoom: 1,
      bathroom: 1,
      bedroom: 1,
      kitchen: 1
    });
    setWindows({
      top: false,
      right: false,
      bottom: false,
      left: false
    });
    setIsDirty(false);
  };
  const handleRoomChange = (room, change) => {
    setRooms(prev => ({
      ...prev,
      [room]: Math.max(1, prev[room] + change)
    }));
  };

  const handleWindowChange = (position) => {
    setWindows(prev => ({
      ...prev,
      [position]: !prev[position]
    }));
  };


  const roomIcons = {
    livingRoom: livingroomIcon,
    bathroom: bathroomIcon,
    bedroom: bedroomIcon,
    kitchen: kitchenIcon
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="p-4 rounded" style={{ backgroundColor: '#F0F0F0' }}>
        <div className="mb-3 row align-items-center">
          <label htmlFor="designName" className="col-2 col-form-label text-start mb-3">Design Name:</label>
          <div className="col-9 mb-3">
            <input
              type="text"
              className="form-control"
              id="designName"
              value={designName}
              onChange={(e) => setDesignName(e.target.value)}
              style={{ width: '250px' }}

              required
            />
          </div>
        </div>

        <div className="mb-3 row align-items-center">
          <label className="col-2 col-form-label text-start mb-3">House Area:</label>
          <div className="col-9 d-flex align-items-center mb-3">
            <input
              type="number"
              className="form-control me-2"
              placeholder="length"
              value={length}
              onChange={(e) => setLength(e.target.value)}
              style={{ width: '100px' }}
              required
            />
            <span className="me-2">m</span>
            <span className="me-2">×</span>
            <input
              type="number"
              className="form-control me-2"
              placeholder="width"
              value={width}
              onChange={(e) => setWidth(e.target.value)}
              style={{ width: '100px' }}
              required
            />
            <span>m</span>
          </div>
        </div>

        <div className="mb-3 row">
          <label className="col-2 col-form-label text-start mb-3">Room Amount:</label>
          <div className="col-9 mb-3">
            <div className="d-flex justify-content-between" style={{ maxWidth: '600px' }}>
              {Object.entries(rooms).map(([room, count]) => (
                <div key={room} className="text-center " style={{
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
                  <div className="btn-group btn-group-sm" role="group">
                    <button type="button" className="btn btn-outline-secondary" onClick={() => handleRoomChange(room, -1)}>-</button>
                    <button type="button" className="btn btn-outline-secondary" disabled>{count}</button>
                    <button type="button" className="btn btn-outline-secondary" onClick={() => handleRoomChange(room, 1)}>+</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mb-3 row">
          <label className="col-2 col-form-label text-start">Windows:</label>
          <div className="col-10">
            <div className="position-relative mb-3" style={{ width: '100%', maxWidth: '400px' }}>
              <img src={designImage} alt="Floor Plan" className="img-fluid" />
              <img 
                src={directionImage} 
                alt="Directions" 
                style={{ 
                  position: 'absolute', 
                  top: '50%', 
                  right: '-30px', 
                  transform: 'translateY(-50%)', 
                  width: '30px' 
                }} 
              />
            </div>
            <div className="d-flex justify-content-between" style={{ maxWidth: '400px' }}>
              {['top', 'right', 'bottom', 'left'].map((position) => (
                <div key={position} className="form-check">
                  <input
                    type="checkbox"
                    className="form-check-input"
                    id={`window-${position}`}
                    checked={windows[position]}
                    onChange={() => handleWindowChange(position)}
                  />
                  <label className="form-check-label" htmlFor={`window-${position}`}>
                    {position}
                  </label>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="text-end">
          <button type="submit" className="btn btn-dark">Submit</button>
        </div>
      </form>

      <CreatingDesignModal show={showModal} loading={loading} />
      

    </>
  );
};

export default DesignForm;