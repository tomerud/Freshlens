import React from 'react';
import './productDetails.scss';

export interface Product {
  name: string;
  image: string;
  amount: number;
  freshness: string;
  expiration: string;
}

interface ProductDetailsProps {
  product: Product;
  onClose: () => void;
}

export const ProductDetails: React.FC<ProductDetailsProps> = ({ product, onClose }) => {
  return (
    <div className="product-details-overlay">
      <div className="product-details">
        <button className="close-btn" onClick={onClose}>X</button>
        <h2>{product.name}</h2>
        <img src={product.image} alt={product.name} className="product-image" />
        <div className="product-info">
          <p><strong>Amount:</strong> {product.amount}</p>
          <p><strong>Freshness:</strong> {product.freshness}</p>
          <p><strong>Expiration Date:</strong> {product.expiration}</p>
          <p><strong>Quantity of Use:</strong> ++</p>
        </div>
      </div>
    </div>
  );
};
