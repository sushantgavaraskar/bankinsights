import React, { useState } from "react";
import { Form, Button, Alert } from "react-bootstrap";
import api from "../services/api";

export default function StatementActions({ onReprocess }) {
  const [statementId, setStatementId] = useState("");
  const [message, setMessage] = useState("");

  const downloadZip = async () => {
    if (!statementId) return alert("Enter statement ID first");
    try {
      const res = await api.get(`/download/statement/${statementId}/`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `statement_${statementId}.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch {
      alert("Download failed");
    }
  };

  const reprocess = async () => {
    if (!statementId) return alert("Enter statement ID");
    try {
      const res = await api.post(`/reprocess_statement/${statementId}/`);
      setMessage(res.data.message || "Reprocessed successfully");
      onReprocess();
    } catch {
      setMessage("Reprocessing failed.");
    }
  };

  return (
    <div className="mt-3">
      <Form className="row g-3">
        <div className="col-md-4">
          <Form.Control
            placeholder="Statement ID"
            type="number"
            onChange={(e) => setStatementId(e.target.value)}
          />
        </div>
        <div className="col-md-4">
          <Button variant="outline-primary" onClick={downloadZip}>
            Download ZIP
          </Button>{" "}
          <Button variant="outline-warning" onClick={reprocess}>
            Reprocess
          </Button>
        </div>
      </Form>
      {message && <Alert className="mt-3">{message}</Alert>}
    </div>
  );
}
