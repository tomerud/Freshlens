import { UserInfo } from './UserInfo';
import { logout } from '../../../firebase';
import { UpdateSubscription } from './UpdateSubscription.tsx';
import { AddFridge } from './AddFridge/AddFridge.tsx';

import './UserProfilePage.scss';

export const UserProfilePage = () => {

  return (
    <>
      <UserInfo />
      <div className="content-container">
        <UpdateSubscription />
        <AddFridge />
      </div>
      <button className="logout-button" onClick={logout}>Logout</button>
    </>
  );
};