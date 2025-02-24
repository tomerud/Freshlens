import _ from "lodash";
import { useEffect, useRef } from "react";

import "./notificationsPopup.scss";

interface NotificationsPopupProps {
  notifications: { id: string; message: string }[];
  isOpen: boolean;
  onClose: () => void;
}

export const NotificationsPopup = ({ notifications, isOpen, onClose }: NotificationsPopupProps) => {
  const popupRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popupRef.current && !popupRef.current.contains(event.target as Node)) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="notification-popup" ref={popupRef}>
      <h4>Notifications</h4>
      {notifications.length > 0 ? (
        <ul>
          {notifications.map((notif) => (
            <li key={notif.id}>{notif.message}</li>
          ))}
        </ul>
      ) : (
        <p>No notifications</p>
      )}
    </div>
  );
};
