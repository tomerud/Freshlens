import { Outlet } from "react-router-dom";
import { Footer } from "../footer";

import "./layout.scss";

export const Layout = () => {
  return (
    <div className="app-container">
      <div className="content">
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};