import React, { useState } from "react";
import { Card, Button, Form, Alert } from "react-bootstrap";
import api from "../services/api";

export default function FileUploader({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setStatus("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("uploaded_file", file);

    try {
      setStatus("Processing...");
      await api.post("/upload/statement/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus("✅ Upload successful.");
      setFile(null);
      onUploadComplete();
    } catch {
      setStatus("❌ Upload failed.");
    }
  };

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <h5>📤 Upload Bank Statement</h5>
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formFile">
            <Form.Control
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
              required
            />
            {file && <small className="text-muted mt-1">Selected: {file.name}</small>}
          </Form.Group>
          <Button className="mt-2" type="submit" disabled={!file || status === "Processing..."}>
            Upload & Process
          </Button>
        </Form>
        {status && (
          <Alert className="mt-3" variant={status.includes("✅") ? "success" : "danger"}>
            {status}
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
}
