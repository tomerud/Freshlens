import { useAuth } from "../../../../contexts/userContext";

import './userInfo.scss'

export const UserInfo = () => {
  const { user } = useAuth();

  return (
    <div className="user-info">
      {user?.photoURL && <img src={user.photoURL} alt="Profile" className="profile-image"/>}
      <h1>{user?.displayName || "Welcome!"}</h1>
      <p className="email">{user?.email}</p>
    </div>
  );
};
