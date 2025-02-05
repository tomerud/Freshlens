import { useParams, useNavigate } from "react-router-dom";
import "./productPage.scss";
import { useQuery } from "@tanstack/react-query";

interface Item {
  product_name: string;
  is_rotten: boolean;
}

const fetchData = async (fridgeId: string, productId: string): Promise<Item[]> => {
  const response = await fetch(`/api/get_all_product_items?fridge_id=${fridgeId}&product_id=${productId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }
  return await response.json();
};

export const ProductPage = () => {
  const navigate = useNavigate();

  const { fridgeId, productId } = useParams<{ fridgeId: string , productId: string }>();

  const { data: items = [], isLoading, error } = useQuery<Item[], Error>({
    queryKey: ['categories', fridgeId, productId],
    queryFn: () => fetchData(fridgeId, productId),
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  if (!items) {
    return <p className="not-found">Product not found.</p>;
  }

  return (
    <div className="product-page">
      
      <header className="product-header">
        <button className="back-button" onClick={() => navigate(-1)}>←</button>
        <h1>{items[0].product_name}</h1>
      </header>
      <ul>
        {items.map((item, index) => (
          <li key={index} style={{ color: item.is_rotten ? "red" : "black" }}>
            {item.product_name} {item.is_rotten ? "🛑 (Rotten)" : "✅ (Fresh)"}
          </li>
        ))}
      </ul>
    </div>
  );
};
