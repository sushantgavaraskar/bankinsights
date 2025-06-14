import { createContext, useContext, useEffect, useState } from "react";
import axios from "../services/api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null
  );
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (authTokens) fetchUserProfile();
  }, [authTokens]);

  const fetchUserProfile = async () => {
    try {
      const res = await axios.get("/auth/profile/");
      setUser(res.data);
    } catch {
      logout();
    }
  };

  const login = async (email, password) => {
    const res = await axios.post("/auth/login/", { email, password });
    localStorage.setItem("authTokens", JSON.stringify(res.data.tokens));
    setAuthTokens(res.data.tokens);
    setUser({ email: res.data.email });
  };

  const register = async (email, full_name, password) => {
    const res = await axios.post("/auth/register/", { email, full_name, password });
    localStorage.setItem("authTokens", JSON.stringify(res.data.tokens));
    setAuthTokens(res.data.tokens);
    setUser({ email: res.data.user.email });
  };

  const logout = () => {
    localStorage.removeItem("authTokens");
    setAuthTokens(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, authTokens, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
