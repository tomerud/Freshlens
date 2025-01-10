import { Routes, Route } from 'react-router-dom';
import { LogInPage } from './UserConnectPage';
import { SignUpPage } from './UserConnectPage/SingUpPage';
import { UserConnectPage } from './UserConnectPage/UserConnectPage';
import { useUser } from '../../../contexts/userContext';

export const UserProfilePage = () => {
  const { user } = useUser();


  return (
    <div>
      <h1>User Profile</h1>
      <Routes>
        <Route path="/" element={<UserConnectPage />} />
        <Route path="login" element={<LogInPage />} />
        <Route path="signup" element={<SignUpPage />} />
      </Routes>
      {user && <h2>{user.fisrtName}</h2>}
    </div>
  );
};