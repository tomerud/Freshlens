import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';

import './shoppingCartLink.scss';

export const ShoppingCartLink = () => {
    const [shoppingCartVisible, setShoppingCartVisible] = useState(false);
  
    useEffect(() => {
      const shoppingCartTimeout = setTimeout(() => setShoppingCartVisible(true), 300); // Animate shopping cart icon
  
      return () => {
        clearTimeout(shoppingCartTimeout);
      };
    }, []);

    return (
      <div>
        <p className="card-label">Shopping Cart</p>
        <Link to={`/shoppingCart/`} className="card">
          <img 
            src='/icons/shopping-cart.png' 
            alt="Shopping Cart" 
            className={`card-icon cart-icon-animated ${shoppingCartVisible ? 'cart-icon-visible' : ''}`} 
          />
        </Link>
    </div>
    );
};
