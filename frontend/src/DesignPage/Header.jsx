import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Modal, Button } from 'react-bootstrap';
import homeIcon from '../assets/home.png';
import penIcon from '../assets/pen-tool.png';
import userIcon from '../assets/user.png';

const Header = ({ onNewDesign, isDesignFormDirty, currentDesign }) => {
    const [showModal, setShowModal] = useState(false);

    const handleNewDesign = () => {
        if (currentDesign) {
            // If in InfoForm, directly execute onNewDesign
            onNewDesign();
        } else if (isDesignFormDirty) {
            // If in DesignForm and there's content, show Modal
            setShowModal(true);
        } else {
            // If in DesignForm but no content, directly execute onNewDesign
            onNewDesign();
        }
    };

    const handleConfirmNewDesign = () => {
        setShowModal(false);
        onNewDesign();
    };

    return (
        <>
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                <h2>Create Your Design</h2>
                <div className="d-flex align-items-center">
                    <button 
                        className="btn btn-dark rounded-pill d-flex align-items-center me-3"
                        onClick={handleNewDesign}
                    >
                        <img src={penIcon} alt="New Design" style={{ width: '20px', height: '20px', marginRight: '5px' }} />
                        New Design
                    </button>
                    <Link to="/" className="text-decoration-none me-3">
                        <img src={homeIcon} alt="Home" style={{ width: '24px', height: '24px' }} />
                    </Link>
                    <img src={userIcon} alt="User" style={{ width: '32px', height: '32px' }} />
                </div>
            </div>

            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Unsaved Changes</Modal.Title>
                </Modal.Header>
                <Modal.Body>You have unsaved changes. Are you sure you want to start a new design?</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Cancel
                    </Button>
                    <Button variant="primary" onClick={handleConfirmNewDesign}>
                        Start New Design
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
};

export default Header;