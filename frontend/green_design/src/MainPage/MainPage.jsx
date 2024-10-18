import React from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import UserAccountMenu from '../component/UserAccountMenu';

const MainPage = () => {
    return (
        <div className="min-vh-100 d-flex flex-column position-relative overflow-hidden">
            {/* 新增的頂部半透明黑色bar */}
            <div className="position-absolute top-0 start-0 end-0" style={{
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                height: '70px',
                zIndex: 10
            }}></div>

            {/* 背景图片 */}
            <div className="position-absolute top-0 start-0 end-0 bottom-0" style={{
                backgroundImage: 'url("/src/assets/pic6.png")',
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                zIndex: 0
            }}></div>
            {/* 頂部導航欄 */}
            <nav className="navbar navbar-expand-lg navbar-dark bg-transparent pt-3" style={{ zIndex: 20 }}>
                <div className="container-fluid">
                    <div className="collapse navbar-collapse justify-content-between" id="navbarNav">
                        <ul className="navbar-nav">
                            <li className="nav-item"><Link className="nav-link text-white" to="/">Home</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/about">About</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/real-estate">Real Estate</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/construction">Construction</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/consultancy">Consultancy</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/contact">Contact Us</Link></li>
                        </ul>
                        <UserAccountMenu />
                    </div>
                </div>
            </nav>

            {/* 主要內容區 */}
            <main className="container-fluid flex-grow-1 d-flex flex-column mt-5" style={{ zIndex: 20 }}>
                <div className="row mt-5">
                    <div className="col-md-6">
                        <h1 className="display-4 text-white mb-2 mt-5">Green Building Solutions</h1>
                        <h3 className="text-white mb-4">Designing for a Sustainable Future</h3>
                        <Link to="/design" className="btn rounded-pill text-white" style={{
                            backgroundColor: '#1F1F1F',
                            border: '2px solid #000000',
                            padding: '10px 20px',
                            fontSize: '1.1rem',
                            fontWeight: 'bold'
                        }}>
                            Start Your Green Design
                        </Link>
                    </div>
                </div>
            </main>             

            {/* 右下角文字，位於白色區域 */}




            <div className="position-absolute bottom-0 end-0 p-4 text-end bg-white bg-opacity-75 rounded-top-left" style={{ zIndex: 10 }}>
                <h2 className="text-success mb-2">Towards Net Zero 2050</h2>
                <h3 className="text-success mb-3">Innovative Green Building Design</h3>
                <ul className="list-unstyled text-success">
                    <li>✓ Optimal Layout Planning</li>
                    <li>✓ Environmental Sensor Integration</li>
                    <li>✓ Energy Efficiency Analysis</li>
                </ul>
            </div>
        </div>
    );
};

export default MainPage;