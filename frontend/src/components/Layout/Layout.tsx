import { Outlet } from "react-router-dom";
import { PhoneHeader } from "../phoneHeader";
import { Footer } from "../footer";

import "./layout.scss";

export const Layout = () => {
  return (
    <div className="app-container">
      <PhoneHeader />
      <div className="content">
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};