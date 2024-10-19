import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainPage from './MainPage/MainPage';
import DesignPage from './DesignPage/DesignPage';
import LoginRegistrationForm from './LoginPage/LoginRegistrationForm';


const App = () => {
  return (
    <Router>
        <Routes>
          <Route path="/main" element={<MainPage />} />
          <Route path="/design" element={<DesignPage />} />
          <Route path="/" element={<LoginRegistrationForm />} />
          {/* 其他路由可以在這裡添加 */}
        </Routes>
    </Router>
  );
};

export default App;