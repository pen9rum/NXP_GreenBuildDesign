import React, { useEffect, useState } from 'react';
import { collection, query, orderBy, limit, onSnapshot } from 'firebase/firestore';
import { db } from '../config/firebase';

const Sidebar = ({ onSelectDesign, onMouseEnter, onMouseLeave }) => {
  const [designs, setDesigns] = useState([]);

  useEffect(() => {
    const designsRef = collection(db, 'all_designs');
    const q = query(designsRef, orderBy('createdAt', 'desc'), limit(10));

    const unsubscribe = onSnapshot(q, (querySnapshot) => {
      const designsData = querySnapshot.docs.map(doc => ({
        id: doc.id,
        designName: doc.data().designName,  // 使用 doc.data() 獲取字段
        imageUrl: doc.data().imageUrl,  
        // ...doc.data()
      }));
      setDesigns(designsData);
    });

    return () => unsubscribe();
  }, []);

  return (
    <nav 
      className="col-md-3 col-lg-2 sidebar shadow-lg p-0 d-flex flex-column" 
      style={{ 
        backgroundColor: 'rgba(64, 64, 64, 0.7)',
        height: '100vh',
        position: 'sticky',
        top: 0,
      }}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <div className="px-3 pt-3 flex-grow-1 overflow-auto">
        <h5 className="sidebar-heading d-flex justify-content-between align-items-center mt-2 mb-2 text-muted">
          <span className='text-white'>History</span>
        </h5>
        <ul className="nav flex-column">
          {designs.length > 0 ? (
            designs.map((design) => (
              <li key={design.id} className="nav-item mb-3">
                <button
                  className="nav-link btn btn-link text-start p-0"
                  onClick={() => onSelectDesign(design)}
                >
                  <div className="p-2 rounded" style={{backgroundColor:'#D9D9D9'}}>
                    <img src={design.imageUrl} alt="Design" className="img-fluid mb-2" />
                    <div className="text-black text-center">{design.designName}</div>
                  </div>
                </button>
              </li>
            ))
          ) : (
            <li className="nav-item">
              <span className="nav-link text-muted">
                No designs found
              </span>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Sidebar;