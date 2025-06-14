import React from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FaHome, FaChartPie, FaFileInvoice, FaTools, FaKey, FaSignOutAlt } from "react-icons/fa";

export default function Sidebar() {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <div className="sidebar bg-teal text-white p-3" style={{ width: "220px", minHeight: "100vh" }}>
      <h4 className="text-white mb-4">💰 TransactIQ</h4>
      <ul className="nav flex-column">
        <li className="nav-item">
          <NavLink to="/dashboard" className="nav-link text-white">
            <FaHome className="me-2" /> Dashboard
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/dashboard#insights" className="nav-link text-white">
            <FaChartPie className="me-2" /> Insights
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/dashboard#transactions" className="nav-link text-white">
            <FaFileInvoice className="me-2" /> Transactions
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/dashboard#tools" className="nav-link text-white">
            <FaTools className="me-2" /> Tools
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/change-password" className="nav-link text-white">
            <FaKey className="me-2" /> Change Password
          </NavLink>
        </li>
        <li className="nav-item mt-3">
          <button className="btn btn-outline-light w-100" onClick={logout}>
            <FaSignOutAlt className="me-2" /> Logout
          </button>
        </li>
      </ul>
    </div>
  );
}
