
import { Link, useLocation } from 'react-router-dom';
import './footer.scss'

const navItems = [
  { path: "/", icon: "home", alt: "Home Icon" },
  { path: "/cameras", icon: "camera", alt: "Camera Icon" },
  { path: "/fridges", icon: "list", alt: "Fridge Icon", isPrefix: true },
  { path: "/user", icon: "user", alt: "User Icon", isPrefix: true },
];

export const Footer = () => {
  const location = useLocation();

  return (
    <div className="footer">
      {navItems.map(({ path, icon, alt, isPrefix }) => {
        const isActive = isPrefix ? location.pathname.startsWith(path) : location.pathname === path;
        return (
          <Link key={path} to={path} className="footer-item">
            <img src={`/icons/${icon}${isActive ? "-active" : ""}.svg`} alt={alt} />
          </Link>
        );
      })}
    </div>
  );
};


