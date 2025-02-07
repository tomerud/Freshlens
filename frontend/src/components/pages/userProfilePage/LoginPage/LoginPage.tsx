import { useEffect } from 'react';
import { signInWithGoogle } from '../../../../firebase';
import { useNavigate } from "react-router-dom";
import { useAuth } from '../../../../contexts/userContext';

import './loginPage.scss';


export const LoginPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) navigate("/");
  }, [user, navigate]);

  return (
  <div className="login-container">
      <p>Please sign in with Google to continue.</p>
      <button onClick={signInWithGoogle} className="google-signin-btn">
        Sign in with Google
      </button>
    </div>
  );
};