import React from 'react';
import { Modal } from 'react-bootstrap';
import loadingImage from '../assets/Pic4.webp';

const CreatingDesignModal = ({ show, loading }) => {
  return (
    <Modal 
      show={show} 
      centered 
      backdrop="static" 
      keyboard={false}
      size="sm"
    >
      <Modal.Body className="text-center p-3">
        <h4 className="mb-3">Creating...</h4>
        <img
          src={loadingImage}
          alt="Creating design"
          className="img-fluid mb-3"
          style={{ maxWidth: '200px', maxHeight: '200px' }}
        />
        <h5 className="mb-0">
          {loading ? "Your design is being created. Please wait..." : "Design created successfully!"}
        </h5>
      </Modal.Body>
    </Modal>
  );
};

export default CreatingDesignModal;