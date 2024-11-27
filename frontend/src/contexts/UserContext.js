import { createContext, useContext, useState } from "react";

export const userContext = createContext({
  user: null,
  setUser: () => {},
});

export const UserContextProvider = ({ children }) => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("User")));
  console.log(JSON.parse(localStorage.getItem("User")));

  return (
    <userContext.Provider value={{ user, setUser }}>
      {children}
    </userContext.Provider>
  );
};

export const useUser = () => useContext(userContext);
