import { useState } from "react";
import { FridgeHeader } from "../../allFridgesPage/fridgeHeader";
import "./shoppingCart.scss";

interface ShoppingItem {
  id: number;
  name: string;
  checked: boolean;
}

export const ShoppingCart = () => {
  const [shoppingCart, setShoppingCart] = useState<ShoppingItem[]>([
    { id: 1, name: "Cheddar Cheese", checked: false },
    { id: 2, name: "Soy Milk", checked: false },
    { id: 3, name: "Tomatoes (2)", checked: false },
    { id: 4, name: "Whole Wheat Bread", checked: false },
    { id: 5, name: "Eggs (12-pack)", checked: false },
    { id: 6, name: "Carrots (5)", checked: false },
    { id: 7, name: "Red Onions (2)", checked: false },
    { id: 8, name: "Bell Peppers (3)", checked: false },
    { id: 9, name: "Romaine Lettuce", checked: false },
    { id: 10, name: "Bananas (6)", checked: false },
    { id: 11, name: "Ground Coffee", checked: false },
    { id: 12, name: "Olive Oil", checked: false }
  ]);

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
              <span className="shopping-name">{item.name}</span>
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
