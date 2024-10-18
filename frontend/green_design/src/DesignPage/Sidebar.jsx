import React, { useEffect, useState} from 'react';
import designImage from '../assets/design.jpeg';
import axios from 'axios';


const Sidebar = ({ designs: initialDesigns,onSelectDesign }) => {

  const [designs, setDesigns] = useState(initialDesigns || []); // 初始化本地設計資料

    useEffect(() => {
        const fetchDesigns = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/getHistoryDesigns');
                setDesigns(response.data);
            } catch (error) {
                console.error('Error fetching designs:', error);
            }
        };
        // 只有當本地設計資料為空時，才從 API 獲取
        if (!designs.length) {
            fetchDesigns();
        }
    }, []); // 只在組件掛載時執行


  return (
    <nav className="col-md-3 col-lg-2 d-md-block sidebar shadow-lg">
      <div className="position-sticky pt-3">
        <h3 className="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
          <span>History</span>
        </h3>
        <hr/>
        <ul className="nav flex-column">
          {designs.length > 0 ? (
            designs.map((design) => (
              <li key={design.id} className="nav-item mb-3">
                <button
                  className="nav-link btn btn-link text-start p-0"
                  onClick={() => onSelectDesign(design)}
                >
                  <div className="p-2 rounded" style={{backgroundColor:'#D9D9D9'}}>
                    <img src={designImage} alt="Design" className="img-fluid mb-2" />
                    <div className="text-black text-center">{design.designName}</div>
                  </div>
                </button>
              </li>
            ))
          ) : (
            <li className="nav-item">
              <span className="nav-link text-muted">
                Not Found
              </span>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Sidebar;