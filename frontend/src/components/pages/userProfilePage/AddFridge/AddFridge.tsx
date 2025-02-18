import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useAuth } from "../../../../contexts/userContext";
import "./AddFridge.scss";

const addNewFridge = async (userId: string, newFridgeName: string): Promise<void> => {
  const response = await fetch("/api/add_fridge", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, fridge_name: newFridgeName }),
  });

  if (!response.ok) {
    throw new Error(`Failed to add fridge: ${response.status}`);
  }

  return response.json();
};

export const AddFridge = () => {
  const { user } = useAuth();
  const [fridgeName, setFridgeName] = useState("");
  const [successMessage, setSuccessMessage] = useState<string | null>(null);


  const { mutate: addFridge, isPending, error } = useMutation<void, Error, { newFridgeName: string }>({
    mutationFn: ({ newFridgeName }) => {
      if (!user) throw new Error("User is not logged in");
      return addNewFridge(user.uid, newFridgeName);
    },

    onSuccess: () => {setFridgeName("");      
      setSuccessMessage("Fridge added successfully!");
      setTimeout(() => setSuccessMessage(null), 2000);
    }
  });

  return (
    <div className="add-fridge-card">
      <h4 className="add-fridge-subtitle">Add a New Fridge</h4>
      <div className="input-container">
        <input
          type="text"
          placeholder="Enter fridge name..."
          value={fridgeName}
          onChange={(e) => setFridgeName(e.target.value)}
          disabled={isPending}
        />
        <button className="add-fridge-button" onClick={() => addFridge({ newFridgeName: fridgeName })} disabled={isPending}>+</button>
      </div>
      {successMessage && <p className="success-text">{successMessage}</p>}
      {error && <p className="error-text">Error: {error.message}</p>}
    </div>
  );
};
