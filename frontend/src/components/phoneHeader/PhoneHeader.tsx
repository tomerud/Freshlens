import { useState, useEffect } from "react";

import "./phoneHeader.scss";

export const PhoneHeader = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date());
    }, 1000 * 60); 

    return () => clearInterval(interval);
  }, []);

  const formattedTime = time.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });

  return (
    <div className="status-bar">
      <span className="time">{formattedTime}</span>
      <img className="icons" src="/icons/phone-header-icons.jpg" alt="Signal Icon" />
    </div>
  );
};
