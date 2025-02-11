import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNotifications } from "./useNotifications";
import "./notifications.scss";

export const Notifications = () => {
  const { notifications, isLoading, error } = useNotifications();
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (notifications.length < 2) return;

    const interval = setInterval(() => {
      setIndex((prevIndex) => (prevIndex + 1) % notifications.length);
    }, 3000);

    return () => clearInterval(interval);
  }, [notifications]);

  if (isLoading) return <p>Loading notifications...</p>;
  if (error) return <p>Error: {error}</p>;
  if (notifications.length === 0) return <p>No notifications</p>;

  return (
    <div className="notification-container">
      <AnimatePresence mode="wait">
        <motion.div
          key={notifications[index].id}
          className="notification-box"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          transition={{ duration: 0.5 }}
        >
          <p>{notifications[index].message}</p>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
