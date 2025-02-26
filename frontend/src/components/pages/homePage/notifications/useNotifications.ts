import { useEffect, useState } from "react";
import { useAuth } from "../../../../contexts/userContext";

interface Notification {
  id: string;
  message: string;
  timestamp: string;
}

export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`/api/get_notifications?user_id=${user?.uid}`);
        if (!response.ok) {
          throw new Error("Failed to fetch notifications");
        }
        const data: Notification[] = await response.json();
        setNotifications(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setIsLoading(false);
      }
    };

    fetchNotifications();
  }, [user?.uid]);

  const refreshNotifications = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`/api/get_notifications?user_id=${user?.uid}`);
      if (!response.ok) {
        throw new Error("Failed to refresh notifications");
      }
      const data: Notification[] = await response.json();
      setNotifications(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  };

  return { notifications, isLoading, error, refreshNotifications };
};
