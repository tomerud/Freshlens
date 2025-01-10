import { createContext, useContext, useState, ReactNode } from 'react';

// Define the shape of the user context
interface User {
  fisrtName: string;
  lastName: string;
  email: string;
  subscription: string;
}

interface UserContextType {
  user: User | null;
  setUser: (user: User) => void;
  clearUser: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider = ({ children }: UserProviderProps): ReactNode => {
  const [user, setUserState] = useState<User | null>(null);

  const setUser = (user: User) => setUserState(user);

  const clearUser = () => setUserState(null);

  return (
    <UserContext.Provider value={{ user, setUser, clearUser }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
