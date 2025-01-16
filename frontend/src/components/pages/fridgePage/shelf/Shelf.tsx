import { useParams } from 'react-router-dom';
import './shelf.scss';
import { useState } from 'react';
import { ProductDetails } from './productDetails';
import { Product } from './productDetails/ProductDetails';

export const Shelf = () => {
  const { shelfName } = useParams<{ shelfName: string }>();
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null); // Type for selected product
  const [showPopup, setShowPopup] = useState(false); // Boolean state for pop-up visibility

  const products: { [key: string]: Product[] } = {
    vegetables: [
      { name: 'CUCUMBERS', image: '/products/cucumbers.jpg', amount: 15, freshness: '42%', expiration: '01/12' },
      { name: 'TOMATOS', image: '/products/tomatos.jpg', amount: 10, freshness: '60%', expiration: '01/15' },
      { name: 'LEMONS', image: '/products/lemons.jpg', amount: 8, freshness: '75%', expiration: '01/18' },
      { name: 'KALE', image: '/products/kale.jpg', amount: 5, freshness: '50%', expiration: '01/10' },
      { name: 'ONION', image: '/products/onion.png', amount: 7, freshness: '30%', expiration: '01/09' },
    ],
    fruit: [
      { name: 'APPLE', image: '/products/apple.jpg', amount: 12, freshness: '80%', expiration: '01/20' },
      { name: 'BANANAS', image: '/products/bananas.jpg', amount: 6, freshness: '65%', expiration: '01/14' },
      { name: 'ORANGES', image: '/products/oranges.jpg', amount: 10, freshness: '70%', expiration: '01/19' },
    ],
    dairy: [
      { name: 'MILK', image: '/milk.png', amount: 3, freshness: '90%', expiration: '01/07' },
      { name: 'CHEESE', image: '/cheese.png', amount: 5, freshness: '85%', expiration: '01/25' },
      { name: 'YOGURT', image: '/yogurt.png', amount: 4, freshness: '50%', expiration: '01/12' },
    ],
    sauces: [
      { name: 'KETCHUP', image: '/ketchup.png', amount: 2, freshness: '95%', expiration: '02/01' },
      { name: 'MAYO', image: '/mayo.png', amount: 1, freshness: '80%', expiration: '01/30' },
      { name: 'BBQ SAUCE', image: '/bbq.png', amount: 3, freshness: '70%', expiration: '01/28' },
    ],
    'fish & meat': [
      { name: 'SALMON', image: '/salmon.png', amount: 2, freshness: '55%', expiration: '01/08' },
      { name: 'CHICKEN', image: '/chicken.png', amount: 4, freshness: '60%', expiration: '01/12' },
      { name: 'STEAK', image: '/steak.png', amount: 3, freshness: '50%', expiration: '01/10' },
    ],
  };
  

  const handleProductClick = (product: Product) => {
    setSelectedProduct(product); // Set the clicked product
    setShowPopup(true); // Show the pop-up
  };

  const closePopup = () => {
    setShowPopup(false); // Close the pop-up
    setSelectedProduct(null); // Reset the selected product
  };

  const shelfProducts = products[shelfName || ''];

  return (
    <div className="shelf">
      <h2>Products on Shelf: {shelfName?.toUpperCase()}</h2>

      {shelfProducts ? (
        <div className="category">
          <div className="product-list">
            {shelfProducts.map((item) => (
              <div
                key={item.name}
                className="product-card"
                onClick={() => handleProductClick(item)} // Pass full Product object
              >
                <p>{item.name}</p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <p>No products found for this shelf.</p>
      )}

      {showPopup && selectedProduct && (
        <ProductDetails product={selectedProduct} onClose={closePopup} />
      )}
    </div>
  );
};
