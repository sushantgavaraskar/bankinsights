import React, { useEffect, useState } from "react";
import { Tabs, Tab, Spinner, Alert } from "react-bootstrap";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import InsightCards from "../components/InsightCards";
import ChartsSection from "../components/ChartsSection";
import FileUploader from "../components/FileUploader";
import TransactionTable from "../components/TransactionTable";
import StatementActions from "../components/StatementActions";

export default function Dashboard() {
  const { user } = useAuth();
  const [insights, setInsights] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadInsights = async () => {
    try {
      const res = await api.get("/insights/");
      setInsights(res.data);
    } catch (err) {
      console.error("Failed to load insights:", err);
    }
  };

  const loadTransactions = async (query = "") => {
    try {
      const res = await api.get(`/transactions/${query}`);
      setTransactions(res.data);
    } catch (err) {
      console.error("Failed to load transactions:", err);
    } finally {
      setLoading(false);
    }
  };

  const refreshAll = async () => {
    setLoading(true);
    await loadTransactions();
    await loadInsights();
  };

  useEffect(() => {
    refreshAll();
  }, []);

  return (
    <div className="container mt-4">
      <h3>Welcome, {user?.email}</h3>
      <FileUploader onUploadComplete={refreshAll} />

      <Tabs defaultActiveKey="insights" className="my-3">
        <Tab eventKey="insights" title="💡 Financial Insights">
          {insights ? (
            <>
              <InsightCards insights={insights} />
              <ChartsSection insights={insights} />
            </>
          ) : (
            <Spinner animation="border" />
          )}
        </Tab>

        <Tab eventKey="transactions" title="📄 Transactions">
          {loading ? (
            <Spinner animation="border" />
          ) : transactions.length === 0 ? (
            <Alert variant="info">No transactions found.</Alert>
          ) : (
            <TransactionTable transactions={transactions} />
          )}
        </Tab>

        <Tab eventKey="tools" title="🧰 Statement Tools">
          <StatementActions onReprocess={refreshAll} />
        </Tab>
      </Tabs>
    </div>
  );
}
