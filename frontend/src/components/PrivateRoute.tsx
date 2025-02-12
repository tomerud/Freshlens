import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/userContext";
import { Loader } from "./loader";

export const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  const { user, loading } = useAuth();

  if (loading) return <Loader />;

  return user ? children : <Navigate to="/login" replace />;
};
