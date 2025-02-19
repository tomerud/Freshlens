import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { Loader } from "../../../../../../loader";

import "./priceData.scss";


interface ProductPriceData {
  product_name: string;
  avg_price: number;
}

const fetchData = async (productId: string): Promise<ProductPriceData> => {
  const response = await fetch(`/api/get_product_price?product_id=${productId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }

  return await response.json();
};

export const PriceData = () => {
  const { productId } = useParams<{ productId: string }>();

  const { data: productPrice, isLoading, error } = useQuery<ProductPriceData, Error>({
    queryKey: ["productPrice", productId],
    queryFn: () => fetchData(productId!),
  });

  if (isLoading) return <Loader />;
  if (error) return <div>Error: {error.message}</div>;

  const formattedPrice =
    productPrice?.avg_price !== null && !isNaN(Number(productPrice?.avg_price))
      ? `$${Number(productPrice?.avg_price).toFixed(2)}`
      : "Price not available";
  
  return (
      <div className="price-container">
        <span>Average Price:</span>
        <span className={`price-value ${productPrice?.avg_price ? "valid" : "invalid"}`}>
          {formattedPrice}
        </span>
      </div>
  );
};
