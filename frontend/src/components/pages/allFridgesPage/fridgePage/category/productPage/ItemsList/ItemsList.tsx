import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { Loader } from "../../../../../../loader";

import "./itemsList.scss";

interface Item {
  item_id: string;
  is_rotten: boolean;
  date_entered: string;
  anticipated_expiry_date: string;
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString("en-GB", {
    weekday: "short", // "Sat"
    day: "2-digit",   // "15"
    month: "short",   // "Feb"
    year: "numeric"   // "2025"
  });
};

const fetchData = async (fridgeId: string, productId: string): Promise<Item[]> => {
  const response = await fetch(`/api/get_all_product_items?fridge_id=${fridgeId}&product_id=${productId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }

  const data = await response.json();

  return data.map((item: Item) => ({
    ...item,
    date_entered: formatDate(item.date_entered),  
    anticipated_expiry_date: formatDate(item.anticipated_expiry_date),
  }));
};

export const ItemsList = () => {
  const { fridgeId, productId } = useParams<{ fridgeId: string; productId: string }>();

  const { data: items = [], isLoading, error } = useQuery<Item[], Error>({
    queryKey: ["categories", fridgeId, productId],
    queryFn: () => fetchData(fridgeId!, productId!),
  });

  if (isLoading) return <Loader />;
  if (error) return <p className="error">Error: {error.message}</p>;

  if (!items.length) {
    return <p className="not-found">No items found for this product.</p>;
  }

  return (
    <div className="items-container">
      <h4 className="items-title">Items In Your Fridge</h4>
      <ul className="items-list">
        {items.map((item, index) => (
          <li key={index} className="item-card">
            <div className="item-header">
              {item.is_rotten ? (
                <img src="/icons/rotten.png" alt="rotten" className="status-icon" />
              ) : (
                <img src="/icons/fresh.png" alt="Cancel" className="status-icon"/>
              )}
              <div className="item-info">
                <span><strong>Entered:</strong> {item.date_entered}</span>
                <span><strong>Expires:</strong> {item.anticipated_expiry_date}</span>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};
