import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from './Sidebar';
import Header from './Header';
import DesignForm from './DesignForm';
import InfoForm from './InfoForm';
import CreatingDesignModal from './CreatingDesignModal';
import Forest from '../assets/forest.webp';

const DesignPage = () => {
    const [isDirty, setIsDirty] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [resetKey, setResetKey] = useState(0);
    const [designs, setDesigns] = useState([]);
    const [currentDesign, setCurrentDesign] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [showSplash, setShowSplash] = useState(true);
    const [showSidebar, setShowSidebar] = useState(false);

    useEffect(() => {
        console.log('Splash screen should be visible');
        const timer = setTimeout(() => {
            console.log('Hiding splash screen');
            setShowSplash(false);
        }, 2000);

        return () => clearTimeout(timer);
    }, []);

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
        }, 30000);
    };

    const handleNewDesign = () => {
        setCurrentDesign(null);
        setIsDirty(false);
        setResetKey(prevKey => prevKey + 1);
    };

    const handleSelectDesign = (design) => {
        setCurrentDesign(design);
        setShowSidebar(false);
    };

    const handleSidebarMouseEnter = () => {
        setShowSidebar(true);
    };

    const handleSidebarMouseLeave = () => {
        setShowSidebar(false);
    };

    useEffect(() => {
        const fetchDesigns = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/designs');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setDesigns(data);
            } catch (error) {
                console.error('Error fetching designs:', error);
            }
        };
        fetchDesigns();
    }, []);

    if (showSplash) {
        console.log('Rendering splash screen');
        return (
            <div 
                style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    width: '100vw',
                    height: '100vh',
                    backgroundImage: `url(${Forest})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    opacity: 1,
                    transition: 'opacity 1s ease-in-out',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    color: 'white',
                    fontSize: '2rem',
                    textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
                    zIndex: 9999,
                }}
            >
                <p>Loading...</p>
                <img src={Forest} alt="Forest" style={{display: 'none'}} />
            </div>
        );
    }

    console.log('Rendering main content');

    return (
        <div style={{
            backgroundImage: `url(${Forest})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundAttachment: 'fixed',
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column'
        }}>
            <Header
                onNewDesign={handleNewDesign}
                isDesignFormDirty={!currentDesign && isDirty}
                currentDesign={currentDesign}
                onMouseEnter={handleSidebarMouseEnter}
                onMouseLeave={handleSidebarMouseLeave}
            />
            <div className="d-flex flex-grow-1 position-relative">
                <div style={{
                    position: 'fixed',
                    top: '56px', // Adjust based on your header height
                    left: 0,
                    bottom: 0,
                    width: '100%', // Increased from 300px to 400px
                    zIndex: 1000,
                    transform: showSidebar ? 'translateX(0)' : 'translateX(-100%)',
                    transition: 'transform 0.3s ease-in-out'
                }}>
                    <Sidebar
                        designs={designs}
                        onSelectDesign={handleSelectDesign}
                        onMouseEnter={handleSidebarMouseEnter}
                        onMouseLeave={handleSidebarMouseLeave}
                    />
                </div>
                <main style={{
                    flexGrow: 1,
                    padding: '20px',
                    marginRight:'100px',
                    marginLeft: '300px', // Adjusted to match the new sidebar width
                    width: 'calc(100% - 400px)', // Adjusted to match the new sidebar width
                }}>
                    <div style={{
                        backgroundColor: 'rgba(255, 255, 255, 0.8)',
                        borderRadius: '10px',
                        padding: '20px',
                        minHeight: 'calc(100vh - 96px)',
                        maxWidth: '1600px', // Increased from 800px to 1000px
                        margin: '0 auto'
                    }}>
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
                    </div>
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