import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Modal, Button } from 'react-bootstrap';
import homeIcon from '../assets/home.png';
import penIcon from '../assets/pen-tool.png';
import UserAccountMenu from '../component/UserAccountMenu';

const Header = ({ onNewDesign, isDesignFormDirty, currentDesign, onMouseEnter, onMouseLeave }) => {
    const [showModal, setShowModal] = useState(false);
    const navigate = useNavigate();

    const handleNewDesign = () => {
        if (currentDesign) {
            onNewDesign();
        } else if (isDesignFormDirty) {
            setShowModal(true);
        } else {
            onNewDesign();
        }
    };

    const handleConfirmNewDesign = () => {
        setShowModal(false);
        onNewDesign();
    };

    return (
        <>
            <div className="d-flex justify-content-between align-items-center w-100 px-3 py-2"
                 style={{
                    backgroundColor: 'rgba(64, 64, 64, 0.7)',
                    zIndex: 1001
                 }}>
                 <h2 
                    className="m-0 text-white" 
                    onMouseEnter={onMouseEnter}
                    onMouseLeave={onMouseLeave}
                    style={{ cursor: 'pointer' }}
                 >
                    GreenBuilder
                 </h2>
                <div className="d-flex align-items-center">
                    <button 
                        className="btn btn-light rounded-pill d-flex align-items-center me-3"
                        onClick={handleNewDesign}
                    >
                        <img src={penIcon} alt="New Design" style={{ width: '20px', height: '20px', marginRight: '5px' }} />
                        New Design
                    </button>
                    <Link to="/" className="text-decoration-none me-3">
                        <img src={homeIcon} alt="Home" style={{ width: '24px', height: '24px' }} />
                    </Link>
                    <UserAccountMenu />
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