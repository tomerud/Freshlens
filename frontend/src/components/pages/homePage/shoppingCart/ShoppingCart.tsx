import { useEffect, useState } from "react";

import { FridgeHeader } from "../../allFridgesPage/fridgeHeader";
import { useQuery } from "@tanstack/react-query";
import { Loader } from "../../../loader";
import { useAuth } from "../../../../contexts/userContext";

import "./shoppingCart.scss";

interface ShoppingItem {
  id: number;
  product_name: string,
  current_quantity: number,
  weekly_avg: number,
  recommendations_amount: number;
  checked: boolean;
}

const fetchShoppingCartRecommendations = async (userId: string | undefined): Promise<ShoppingItem[]> => {
  const response = await fetch(`/api/get_shopping_cart_recommendations?user_id=${userId}`);
  if (!response.ok) throw new Error("Failed to fetch shopping cart recommendations");
  return response.json();
};

export const ShoppingCart = () => {
  const {user} = useAuth();
  
  const { data, isLoading, error } = useQuery<ShoppingItem[], Error>({
    queryKey: user?.uid ? ["ShoppingCart", user?.uid] : ["ShoppingCart"],
    queryFn: () => fetchShoppingCartRecommendations(user?.uid),
    enabled: !!user?.uid,
  });

  const [shoppingCart, setShoppingCart] = useState<ShoppingItem[]>([]);

  useEffect(() => {
    if (data) {
      setShoppingCart(data);
    }
  }, [data]);

  const toggleChecked = (id: number) => {
    setShoppingCart((prevCart) =>
      prevCart.map((item) =>
        item.id === id ? { ...item, checked: !item.checked } : item
      )
    );
  };

  const handleSubmit = () => {
    setShoppingCart((prevCart) => prevCart.filter((item) => !item.checked));
  };

  if (isLoading) return <Loader />;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <>
      <FridgeHeader title="Shopping Cart" subtitle="Your smart custom shopping list!"/>
      <div className="shopping-container">
        <ul className="shopping-list">
          {shoppingCart.map((item) => (
            <li key={item.id} className={`shopping-item ${item.checked ? "checked" : ""}`} onClick={() => toggleChecked(item.id)}>
              <input
                type="checkbox"
                checked={item.checked}
                readOnly
                className="shopping-checkbox"
              />
              <span className="shopping-name">{item.product_name} ({item.recommendations_amount})</span>
              {item.checked && <span className="checkmark">✔</span>}
            </li>
          ))}
        </ul>
        {shoppingCart.some(item => item.checked) && (
          <button className="submit-button" onClick={handleSubmit}>
            Purchased!
          </button>
        )}
      </div>
    </>
  );
};