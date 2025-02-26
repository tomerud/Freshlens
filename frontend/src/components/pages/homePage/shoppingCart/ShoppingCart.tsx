import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { FridgeHeader } from "../../allFridgesPage/fridgeHeader";
import { Loader } from "../../../loader";

import "./shoppingCart.scss";

interface ShoppingRecommendation {
  product_id: number;
  product: string;
  amount_buy: number;
  amount_will_throw: number;
  recommendation: number;
}

interface ShoppingRecommendationItem extends ShoppingRecommendation {
  checked: boolean;
}

const fetchShoppingCartRecommendations = async (userId: string): Promise<ShoppingRecommendation[]> => {
  const response = await fetch(`/api/get_shopping_cart_recommendations?user_id=${userId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch shopping cart recommendations");
  }
  return response.json();
};

export const ShoppingCart = () => {
  const userId = "0NNRFLhbXJRFk3ER2_iTr8VulFm4"; // Replace with your actual user ID or context-based user ID

  const [shoppingCart, setShoppingCart] = useState<ShoppingRecommendationItem[]>([]);

  const { data, isLoading, error } = useQuery<ShoppingRecommendation[], Error>({
    queryKey: userId ? ["ShoppingCart", userId] : ["ShoppingCart"],
    queryFn: () => fetchShoppingCartRecommendations(userId),
    enabled: !!userId,
  });

  console.log(data)

  useEffect(() => {
    if (data) {
      const itemsWithCheck = data.map((item) => ({
        ...item,
        checked: false,
      }));
      setShoppingCart(itemsWithCheck);
    }
  }, [data]);

  const toggleChecked = (product_id: number) => {
    setShoppingCart((prevCart) =>
      prevCart.map((item) =>
        item.product_id === product_id
          ? { ...item, checked: !item.checked }
          : item
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
      <FridgeHeader title="Shopping Cart" subtitle="Your smart custom shopping list!" />
      <div className="shopping-container">
        <ul className="shopping-list">
          {shoppingCart.map((item) => (
            <li
              key={item.product_id}
              className={`shopping-item ${item.checked ? "checked" : ""}`}
              onClick={() => toggleChecked(item.product_id)}
            >
              <input
                type="checkbox"
                checked={item.checked}
                readOnly
                className="shopping-checkbox"
              />
              <div className="shopping-details">
                <span className="shopping-name">
                  {item.product} (Buy {item.recommendation})
                </span>
                <small className="shopping-reason">
                  We estimate you'll buy {item.amount_buy} but throw out{" "}
                  {item.amount_will_throw}, so we recommend {item.recommendation}.
                </small>
              </div>
              {item.checked && <span className="checkmark">✔</span>}
            </li>
          ))}
        </ul>
        {shoppingCart.some((item) => item.checked) && (
          <button className="submit-button" onClick={handleSubmit}>
            Purchased!
          </button>
        )}
      </div>
    </>
  );
};
