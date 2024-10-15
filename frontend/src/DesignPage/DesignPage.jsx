import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from './Sidebar';
import Header from './Header';
import DesignForm from './DesignForm';
import InfoForm from './InfoForm';
import CreatingDesignModal from './CreatingDesignModal';

const DesignPage = () => {
    const [isDirty, setIsDirty] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [resetKey, setResetKey] = useState(0);
    const [designs, setDesigns] = useState([]);
    const [currentDesign, setCurrentDesign] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleDesignSubmit = (designInfo) => {
        setIsLoading(true);
        setShowModal(true);
        if (currentDesign) {
            setDesigns(prevDesigns => prevDesigns.map(design =>
                design.id === currentDesign.id ? designInfo : design
            ));
        } else {
            setDesigns(prevDesigns => [...prevDesigns, designInfo]);
        }
        setCurrentDesign(designInfo);
        setIsDirty(false);
        setTimeout(() => {
            setShowModal(false);
            setIsLoading(false);
        }, 3000);
    };

    const handleNewDesign = () => {
        setCurrentDesign(null);
        setIsDirty(false);
        setResetKey(prevKey => prevKey + 1);
    };

    const handleSelectDesign = (design) => {
        setCurrentDesign(design);
    };

    useEffect(() => {
        // Fetch designs from API when component mounts
        const fetchDesigns = async () => {
            try {
                const response = await fetch('/api/designs');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setDesigns(data);
            } catch (error) {
                console.error('Error fetching designs:', error);
                // Handle error (e.g., show error message to user)
            }
        };
        fetchDesigns();
    }, []);

    return (
        <div className="container-fluid">
            <div className="row vh-100">
                <Sidebar designs={designs} onSelectDesign={handleSelectDesign} />
                <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4" style={{ backgroundColor: '#F6F6F6' }}>
                    <Header
                        onNewDesign={handleNewDesign}
                        isDesignFormDirty={!currentDesign && isDirty}
                        currentDesign={currentDesign}
                    />
                    {currentDesign ? (
                        <InfoForm designInfo={currentDesign} />
                    ) : (
                        <DesignForm
                            key={resetKey}
                            onSubmit={handleDesignSubmit}
                            initialData={null}
                            isDirty={isDirty}
                            setIsDirty={setIsDirty}
                            setIsLoading={setIsLoading}
                        />
                    )}
                </main>
            </div>
            <CreatingDesignModal
                show={showModal}
                loading={isLoading}
            />
        </div>
    );
};

export default DesignPage;