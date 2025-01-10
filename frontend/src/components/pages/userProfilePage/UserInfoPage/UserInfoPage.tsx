import { useUser } from "../../../../contexts/userContext";

export const UserInfoPage = () => {
  const { user } = useUser();


  return (
    <div>
      <h1>Hello</h1>
      <h2>{user?.name}</h2>
      <h2>{user?.email}</h2>
    </div>
  );
};