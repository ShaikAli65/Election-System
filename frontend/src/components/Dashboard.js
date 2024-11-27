// Dashboard.js
import React, { useEffect } from "react";
import { useAuth } from "./AuthContext";

const Dashboard = () => {
  const { authData } = useAuth();

  // Log authData when Dashboard renders or updates
  useEffect(() => {
    console.log("authData in Dashboard:", authData);
  }, [authData]);

  return (
    <div>
      <h2>Dashboard</h2>
      {authData ? (
        <div>
          <p>Welcome, {authData.username}!</p>
          <p>Your User ID: {authData.userId}</p>
          <p>Your Token: {authData.token}</p>
        </div>
      ) : (
        <p>Please log in to access the dashboard.</p>
      )}
    </div>
  );
};

export default Dashboard;
