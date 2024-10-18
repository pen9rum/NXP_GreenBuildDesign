import React, { useState, useEffect } from 'react';
import { Modal, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import CreatingDesignModal from './CreatingDesignModal';
import bathroomIcon from '../assets/bathroom.png';
import bedroomIcon from '../assets/bedroom.png';
import kitchenIcon from '../assets/kitchen.png';
import livingroomIcon from '../assets/livingroom.png';
import designImage from '../assets/design.jpeg';

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
  const [specialRequest, setSpecialRequest] = useState(initialData?.specialRequest || '');
  const [showModal, setShowModal] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

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
      setSpecialRequest(initialData.specialRequest || '');
    }
  }, [initialData]);

  useEffect(() => {
    const isFormDirty = designName !== '' || length !== '' || width !== '' ||
      Object.values(rooms).some(value => value !== 1) ||
      Object.values(windows).some(value => value === true) ||
      specialRequest !== '';
    setIsDirty(isFormDirty);
  }, [designName, length, width, rooms, windows, specialRequest, setIsDirty]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const designInfo = {
      designName,
      length,
      width,
      rooms,
      windows,
      specialRequest
    };
    setIsLoading(true);
    setShowModal(true);
    try {
      console.log(designInfo)
      const response = await axios.post('/api/designs', designInfo);
      
      onSubmit(response.data);
      setIsDirty(false);
      // Wait for the response before navigating
      setTimeout(() => {
        setShowModal(false);
        setIsLoading(false);
        navigate('/info-form', { state: { designInfo: response.data } });
      }, 3000);
    } catch (error) {
      console.error('Error submitting design:', error);
      setShowModal(false);
      setIsLoading(false);
      // Handle error (e.g., show error message to user)
    }
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
    setSpecialRequest('');
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
        <div className="mb-2 row align-items-center">
          <label htmlFor="designName" className="col-2 col-form-label text-start mb-2">Design Name:</label>
          <div className="col-9 mb-2">
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

        <div className="mb-2 row align-items-center">
          <label className="col-2 col-form-label text-start mb-2">House Area:</label>
          <div className="col-9 d-flex align-items-center mb-2">
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

        <div className="mb-2 row">
          <label className="col-2 col-form-label text-start mb-2">Room Amount:</label>
          <div className="col-9 mb-2">
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

        <div className="mb-2 row">
          <label className="col-2 col-form-label text-start">Windows:</label>
          <div className="col-10">
            <div className="position-relative mb-2" style={{ width: '100%', maxWidth: '400px' }}>
              <img src={designImage} alt="Floor Plan" className="img-fluid" />
            </div>
            <div className="d-flex justify-content-between mb-2" style={{ maxWidth: '400px' }}>
              {['top', 'right', 'bottom', 'left'].map((position) => (
                <div key={position} className="form-check">
                  <input
                    type="checkbox"
                    className="form-check-input"
                    id={`window-${position}`}
                    checked={windows[position]}
                    onChange={() => handleWindowChange(position)}
                  />
                  <label className="form-check-label " htmlFor={`window-${position}`}>
                    {position}
                  </label>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mb-2 row">
          <label htmlFor="specialRequest" className="col-2 col-form-label text-start">Special Request:</label>
          <div className="col-10">
            <textarea
              className="form-control"
              id="specialRequest"
              value={specialRequest}
              onChange={(e) => setSpecialRequest(e.target.value)}
              style={{ width: '100%', minHeight: '100px' }}
              placeholder="Enter any special requests or additional information here..."
            />
          </div>
        </div>

        <div className="text-end">
          <button type="submit" className="btn btn-dark">Submit</button>
        </div>
      </form>

      <CreatingDesignModal show={showModal} loading={isLoading} />
      <Modal show={showConfirmModal} onHide={() => setShowConfirmModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Unsaved Changes</Modal.Title>
        </Modal.Header>
        <Modal.Body>You have unsaved changes. Are you sure you want to start a new design?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowConfirmModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={() => {
            resetForm();
            setShowConfirmModal(false);
          }}>
            Start New Design
          </Button>
        </Modal.Footer>
      </Modal>

    </>
  );
};

export default DesignForm;