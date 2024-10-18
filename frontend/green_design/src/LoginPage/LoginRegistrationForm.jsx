import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Modal } from 'react-bootstrap';
import { initializeApp } from 'firebase/app';
import { 
  getAuth, 
  signInWithPopup, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  GoogleAuthProvider,
  onAuthStateChanged
} from "firebase/auth";
import { firebaseConfig } from "../config/firebase";
import GreenDesign from '../assets/Pic2.jpeg';
import Google from '../assets/google.png';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

const LoginRegistrationForm = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        navigate('/');
      }
    });

    return () => unsubscribe();
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setShowModal(true);
    setError('');

    try {
      if (isLogin) {
        await signInWithEmailAndPassword(auth, email, password);
      } else {
        await createUserWithEmailAndPassword(auth, email, password);
      }
      navigate('/');
    } catch (error) {
      setError(error.message);
    } finally {
      setShowModal(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setShowModal(true);
    setError('');

    const provider = new GoogleAuthProvider();
    provider.setCustomParameters({
      prompt: 'select_account'
    });

    try {
      await signInWithPopup(auth, provider);
      navigate('/');
    } catch (error) {
      setError(error.message);
    } finally {
      setShowModal(false);
    }
  };

  return (
    <div className="container-fluid">
      <div className="row" style={{ minHeight: '100vh' }}>
        <div className="col-md-6 d-flex align-items-center justify-content-center">
          <div className="w-75">
            <h2 className="mb-4 text-center">{isLogin ? 'Sign In' : 'Get Started Now'}</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
              {!isLogin && (
                <div className="mb-3">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
              )}
              <div className="mb-3">
                <input
                  type="email"
                  className="form-control"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <input
                  type="password"
                  className="form-control"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              {!isLogin && (
                <div className="mb-3 form-check">
                  <input
                    type="checkbox"
                    className="form-check-input"
                    id="agreeTerms"
                    checked={agreeTerms}
                    onChange={(e) => setAgreeTerms(e.target.checked)}
                    required
                  />
                  <label className="form-check-label" htmlFor="agreeTerms">
                    I agree to the terms & policy
                  </label>
                </div>
              )}
              <button type="submit" className="btn btn-success w-100">
                {isLogin ? 'Sign In' : 'Sign Up'}
              </button>
            </form>
            <div className="text-center my-3">Or</div>
            <button
              onClick={handleGoogleSignIn}
              className="btn btn-outline-dark w-100"
            >
              <img
                src={Google}
                alt="Google logo"
                style={{ width: '20px', marginRight: '10px' }}
              />
              Sign {isLogin ? 'in' : 'up'} with Google
            </button>
            <div className="text-center mt-3">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <Link to="#" onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? 'Sign Up' : 'Sign In'}
              </Link>
            </div>
          </div>
        </div>
        <div className="col-md-6 bg-light d-flex align-items-center justify-content-center">
          <img
            src={GreenDesign}
            alt="Green energy infographic"
            className="img-fluid"
          />
        </div>
      </div>

      <Modal show={showModal} centered backdrop="static" keyboard={false}>
        <Modal.Body className="text-center">
          <h4>Authenticating...</h4>
          <div className="spinner-border text-success my-3" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>Please wait while we {isLogin ? 'sign you in' : 'create your account'}...</p>
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default LoginRegistrationForm;