import { useEffect, useState } from 'react';
import { buildStyles, CircularProgressbar } from 'react-circular-progressbar';
import { MoneySaveGraph } from './moneySaveGraph';

import './graphSection.scss';
import { Link } from 'react-router-dom';

export const GraphSection = () => {
  const [fridgeFreshness, setPridgeFreshness] = useState(0);
  const [shoppingCartVisible, setShoppingCartVisible] = useState(false);

  useEffect(() => {
    const fridgeFreshnessTimeout = setTimeout(() => setPridgeFreshness(82), 300); // Animate CircularProgressbar
    const hoppingCartTimeout = setTimeout(() => setShoppingCartVisible(true), 300); // Animate shopping cart icon

    return () => {
      clearTimeout(fridgeFreshnessTimeout);
      clearTimeout(hoppingCartTimeout);
    };
  }, []);

  return (
    <>
      <div className="cards-container">
        <div className="card-wrapper">
          <p className="card-label">Shopping Cart</p>
          <Link to={`/shoppingCart/`} className="card">
            <img 
              src='/icons/shopping-cart.png' 
              alt="Shopping Cart" 
              className={`card-icon cart-icon-animated ${shoppingCartVisible ? 'cart-icon-visible' : ''}`} 
            />
          </Link>
        </div>
        <div className="card-wrapper">
          <p className="card-label">Fridge Freshness</p>
          <div className="card">
            <CircularProgressbar 
              value={fridgeFreshness} 
              text={`${fridgeFreshness}%`} 
              styles={buildStyles({
                textSize: '20px',
                pathColor: '#66bb6a',
                textColor: '#000',
                trailColor: '#eee',
              })}
            />
          </div>
        </div>
      </div>

      <MoneySaveGraph />
    </>
  );
};
