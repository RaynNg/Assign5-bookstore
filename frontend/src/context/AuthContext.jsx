import { createContext, useContext, useState, useEffect } from "react";
import { customerService } from "../services";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("customer");
    if (stored) {
      setCustomer(JSON.parse(stored));
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await customerService.login({ username, password });
      const customerData = response.data;
      setCustomer(customerData);
      localStorage.setItem("customer", JSON.stringify(customerData));
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Đăng nhập thất bại",
      };
    }
  };

  const register = async (data) => {
    try {
      const response = await customerService.register(data);
      const customerData = response.data;
      setCustomer(customerData);
      localStorage.setItem("customer", JSON.stringify(customerData));
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || "Đăng ký thất bại",
      };
    }
  };

  const logout = () => {
    setCustomer(null);
    localStorage.removeItem("customer");
  };

  const updateCustomer = (data) => {
    const updated = { ...customer, ...data };
    setCustomer(updated);
    localStorage.setItem("customer", JSON.stringify(updated));
  };

  return (
    <AuthContext.Provider
      value={{
        customer,
        loading,
        login,
        register,
        logout,
        updateCustomer,
        isAuthenticated: !!customer,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
