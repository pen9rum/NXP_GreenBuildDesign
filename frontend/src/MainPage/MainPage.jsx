import React from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

const MainPage = () => {
    return (
        <div className="min-vh-100 d-flex flex-column position-relative overflow-hidden" style={{
            backgroundImage: 'url("/src/assets/pic6.png")',
            backgroundSize: 'cover',
            backgroundPosition: 'center'
        }}>
            {/* 頂部導航欄 */}
            <nav className="navbar navbar-expand-lg navbar-light bg-transparent pt-3">
                <div className="container-fluid">
                    <div className="collapse navbar-collapse justify-content-start" id="navbarNav">
                        <ul className="navbar-nav">
                            <li className="nav-item"><Link className="nav-link text-white" to="/">Home</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/about">About</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/real-estate">Real Estate</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/construction">Construction</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/consultancy">Consultancy</Link></li>
                            <li className="nav-item"><Link className="nav-link text-white" to="/contact">Contact Us</Link></li>
                        </ul>
                    </div>
                </div>
            </nav>

            {/* 主要內容區 */}
            <main className="container-fluid flex-grow-1 d-flex flex-column ">
                <div className="row mt-5">
                    <div className="col-md-6">
                        <h1 className="display-4 text-white mb-2 mt-5">Green Your House</h1>
                        <Link to="/design" className="btn btn-dark rounded-pill">New Design</Link>          </div>
                </div>
            </main>            

            {/* 右下角文字，位於白色區域 */}
            <div className="position-absolute bottom-0 end-0 p-4 text-end" style={{ zIndex: 10 }}>
                <h2 className="text-success mb-2">Be a co-Landlord</h2>
                <h3 className="text-success mb-3">Brick by Brick</h3>
                <button className="btn btn-success rounded-pill">Learn More</button>
            </div>
        </div>
    );
};

export default MainPage;