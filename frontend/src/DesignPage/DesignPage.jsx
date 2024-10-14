import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from './Sidebar';
import Header from './Header';
import DesignForm from './DesignForm';
import InfoForm from './InfoForm';
import CreatingDesignModal from './CreatingDesignModal';
import { useDesignContext } from './DesignContext';
import loadingImage from '../assets/Pic4.webp';

const DesignPage = () => {
    const [isDirty, setIsDirty] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [resetKey, setResetKey] = useState(0); // 新增：用於強制重置 DesignForm

    const { designs, currentDesign, addDesign, updateDesign, selectDesign, clearCurrentDesign } = useDesignContext();

    const handleDesignSubmit = (designInfo) => {
        if (currentDesign) {
            updateDesign(designInfo);
        } else {
            addDesign(designInfo);
        }
        setShowModal(true);
        
        setTimeout(() => {
            setShowModal(false);
        }, 3000);
    };

    const handleNewDesign = () => {
        clearCurrentDesign();
        setIsDirty(false);
        setResetKey(prevKey => prevKey + 1); // 增加 key 以強制重置 DesignForm
    };

    useEffect(() => {
        if (!showModal && currentDesign) {
            setIsDirty(prev => !prev);
        }
    }, [showModal, currentDesign]);

    return (
        <div className="container-fluid">
            <div className="row vh-100">
                <Sidebar designs={designs} onSelectDesign={selectDesign} />
                <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4" style={{ backgroundColor: 'F6F6F6' }}>
                    <Header 
                        onNewDesign={handleNewDesign} 
                        isDesignFormDirty={!currentDesign && isDirty} 
                    />
                    {currentDesign && !showModal ? (
                        <InfoForm designInfo={currentDesign} />
                    ) : (
                        <DesignForm
                            key={resetKey} // 新增：使用 key 來強制重置組件
                            onSubmit={handleDesignSubmit}
                            initialData={null} // 修改：總是傳遞 null 作為初始數據
                            isDirty={isDirty}
                            setIsDirty={setIsDirty}
                        />
                    )}
                </main>
            </div>
            <CreatingDesignModal 
                show={showModal} 
                loading={loadingImage}
            />
        </div>
    );
};

export default DesignPage;