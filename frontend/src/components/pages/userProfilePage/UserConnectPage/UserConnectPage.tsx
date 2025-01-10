import { Link } from 'react-router-dom';

export const UserConnectPage = () => {

  return (
    <div>
      <h2>User Connect</h2>
      <Link to="login">
        <button>Log In</button>
      </Link>
      <Link to="signup">
        <button>Sign Up</button>
      </Link>
    </div>
  );
};