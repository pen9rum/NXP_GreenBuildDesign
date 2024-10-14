import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainPage from './MainPage/MainPage';
import DesignPage from './DesignPage/DesignPage';
import LoginRegistrationForm from './LoginPage/LoginRegistrationForm';
import { DesignProvider } from './DesignPage/DesignContext';


const App = () => {
  return (
    <Router>
      <DesignProvider>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/design" element={<DesignPage />} />
          <Route path="/login" element={<LoginRegistrationForm />} />
          {/* 其他路由可以在這裡添加 */}
        </Routes>
      </DesignProvider>
    </Router>
  );
};

export default App;