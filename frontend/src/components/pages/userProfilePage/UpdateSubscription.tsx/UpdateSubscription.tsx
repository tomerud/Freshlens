import { useMutation } from "@tanstack/react-query";
import { useAuth } from "../../../../contexts/userContext";
import "./updateSubscription.scss";
import { useState } from "react";

const SUBSCRIPTION_OPTIONS = [
  { id: 1, label: "Free", className: "btn free" },
  { id: 2, label: "Plus", className: "btn plus" },
  { id: 3, label: "Premium", className: "btn premium" },
];

const updateUserSubscription = async (userId: string, newSubscriptionId: number): Promise<void> => {
  const response = await fetch("/api/update_user_subscription", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, new_subscription_id: newSubscriptionId }),
  });

  if (!response.ok) {
    throw new Error(`Failed to update subscription: ${response.status}`);
  }

  return response.json();
};

export const UpdateSubscription = () => {
  const { user } = useAuth();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);


  const { mutate: updateSubscription, isPending, error } = useMutation<void, Error, { newSubscriptionId: number }>({
    mutationFn: ({ newSubscriptionId }) => {
      if (!user) throw new Error("User is not logged in");
      return updateUserSubscription(user.uid, newSubscriptionId);
    },

    onSuccess: () => {
      setSuccessMessage("Subscription updated successfully!");
      setTimeout(() => setSuccessMessage(null), 2000);
    },
  });

  return (
    <div className="subscription-card">
    <h4>Update Subscription Plan</h4>
    <div className="buttons">
      {SUBSCRIPTION_OPTIONS.map(({ id, label, className }) => (
        <button
          key={id}
          className={className}
          onClick={() => updateSubscription({ newSubscriptionId: id })}
          disabled={isPending}
        >
          {label}
        </button>
      ))}
    </div>
    {successMessage && <p className="success-text">{successMessage}</p>}

    {error && <p className="error-text">Error: {error.message}</p>}
  </div>
  );
};
