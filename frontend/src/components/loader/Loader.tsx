
import { useEffect, useState } from 'react';
import './loader.scss'


export const Loader = () => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(true), 3000); // Delay to prevent flickering
    return () => clearTimeout(timer);
  }, []);

  return visible ? (
    <div className="loader-container">
      <div className="spinner"></div>
    </div>
  ) : null;
};


