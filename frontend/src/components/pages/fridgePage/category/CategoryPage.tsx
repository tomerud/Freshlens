import { useParams, Link, useNavigate } from "react-router-dom";
import { useState } from "react";
// import { ProductPage } from "./productPage/ProductPage";
import "./categoryPage.scss";
import { useQuery } from "@tanstack/react-query";

interface Product {
  product_id: number;
  product_name: string;
}

const fetchData = async (fridgeId: string, categoryName: string): Promise<Product[]> => {
  const response = await fetch(`/api/get_all_products?fridge_id=${fridgeId}&category_name=${categoryName}`);

  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }
  return await response.json();
};

export const CategoryPage = () => {
  const { fridgeId, categoryName } = useParams<{ fridgeId: string, categoryName: string }>();
  const navigate = useNavigate();

  const { data: Products = [], isLoading, error } = useQuery<Product[], Error>({
    queryKey: ['categories', fridgeId, categoryName],
    queryFn: () => fetchData(fridgeId, categoryName),
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div className="category-page">
      <header className="category-header">
        <button className="back-button" onClick={() => navigate(-1)}>←</button>
        <h1>MY {categoryName?.toUpperCase()}</h1>
      </header>

      {Products ? (
        <div className="product-list">
          {Products.map((product) => (
            <Link key={product.product_id} to={`${product.product_id}`} className="product-item">
              <p>{product.product_name}</p>
            </Link>
          ))}
        </div>
      ) : (
        <p className="no-products">No products found for this category.</p>
      )}
    </div>
  );
};
