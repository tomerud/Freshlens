
import { Link } from 'react-router-dom';
import './footer.scss'

  export const Footer = () => {
  
    return (
      <div className="footer">
        <Link to="/fridge" className="footer-item">
          <img src="./../public/busket.png" alt="Basket Icon" />
        </Link>
        <div className="footer-divider"></div>
        <Link to="/" className="footer-item">
          <img src="./../public/home.png" alt="Home Icon" />
        </Link>
        <div className="footer-divider"></div>
        <Link to="/user" className="footer-item">
          <img src="./../public/person.png" alt="User Icon" />
        </Link>
      </div>
    );
  };


