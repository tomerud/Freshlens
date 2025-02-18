import { useState } from "react";
import { IoNotificationsOutline } from "react-icons/io5";

import { useNotifications } from "../notifications/useNotifications";
import { NotificationsPopup } from "./notificationsPopup";

import "./homePageHeader.scss";

export const HomePageHeader = () => {
  const today = new Date();
  const formattedDate = today.toLocaleDateString("en-US", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });

  const { notifications } = useNotifications();
  const notificationCount = notifications.length;

  const [isPopupOpen, setIsPopupOpen] = useState(false);

  return (
    <header className="homepage-header">
      <div className="header-left">
        <h1 className="app-title">FreshLens</h1>
        <p className="date">{formattedDate}</p>
      </div>
      <div className="header-icons">
        <div className="notification-icon-container" onClick={() => setIsPopupOpen((prev) => !prev)}>
          <IoNotificationsOutline className="icon" />
          {notificationCount > 0 && <span className="notification-badge">{notificationCount}</span>}
        </div>

        <NotificationsPopup
          notifications={notifications}
          isOpen={isPopupOpen}
          onClose={() => setIsPopupOpen(false)}
        />
      </div>
    </header>
  );
};
