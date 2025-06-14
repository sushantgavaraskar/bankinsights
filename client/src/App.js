import React from "react";
import { AuthProvider } from "./context/AuthContext";
import AppRoutes from "./routes";
import Sidebar from "./components/Sidebar";
import "./styles/global.css";

function App() {
  return (
    <AuthProvider>
      <div className="d-flex">
        <Sidebar />
        <div className="flex-grow-1 p-3 bg-light min-vh-100">
          <AppRoutes />
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;
