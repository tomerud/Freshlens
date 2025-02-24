import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { FridgeHeader } from "../../../fridgeHeader";
import { ItemsList } from "./ItemsList";
import { Loader } from "../../../../../loader";
import { PriceData } from "./PriceData";
import { NutrientData } from "./NutrientData";
import { TipsSection } from "../../../../../TipsSection";

import "./productPage.scss";

interface Product {
  product_id: string;
  product_name: string;
}

const fetchData = async (productId: string): Promise<Product> => {
  const response = await fetch(`/api/get_product_name?product_id=${productId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }

  return await response.json();
};

const getProductImage = (product: Product) => {
  const imageMap: Record<string, string> = {
    "kale": "/products/kale.jpg",
    "cucumber": "/products/cucumber.png",
    "eggplant": "/products/eggplant.webp",
    "ginger": "/products/ginger.webp",
    "lemon": "/products/lemon.png",
    "tomato": "/products/tomato.png",
    "swiss cheese": "/products/swiss-cheese.jpg",
    "coffee creamer": "/products/coffee-creamer.jpg",
    "yogurt": "/products/yogurt.jpg",
    "ricotta cheese": "/products/ricotta.jpg",
  };
  return imageMap[product.product_name.toLowerCase()] || null;
};

export const ProductPage = () => {
  const { productId } = useParams<{ productId: string }>();

  const { data: product, isLoading, error } = useQuery<Product, Error>({
    queryKey: ["ProductName", productId],
    queryFn: () => fetchData(productId!),
  });

  if (isLoading) return <Loader />;
  if (error) return <div>Error: {error.message}</div>;

  const productImage = getProductImage(product!);

  return (
    <>
      <FridgeHeader title={product!.product_name} subtitle="Everything you need to know" />
      
      {productImage && (
        <div className="product-image-container">
          <img src={productImage} alt={product!.product_name} className="product-image" />
        </div>
      )}

      <ItemsList />
      <NutrientData />
      <PriceData />
      <TipsSection productId={productId} addedTitle={product!.product_name} classname="no-border" />
    </>
  );
};
