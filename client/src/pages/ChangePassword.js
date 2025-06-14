import React, { useState } from "react";
import { Button, Card, Container, Form, Alert } from "react-bootstrap";
import api from "../services/api";

export default function ChangePassword() {
  const [formData, setFormData] = useState({ current_password: "", new_password: "" });
  const [message, setMessage] = useState("");

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/auth/change-password/", formData);
      setMessage(res.data.message || "Password changed successfully.");
    } catch {
      setMessage("Password change failed. Please check credentials.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: "80vh" }}>
      <Card className="p-4" style={{ minWidth: "320px", maxWidth: "400px", width: "100%" }}>
        <h4 className="mb-3 text-center">🔒 Change Password</h4>
        <Form onSubmit={handleSubmit}>
          {message && <Alert variant={message.includes("success") ? "success" : "danger"}>{message}</Alert>}
          <Form.Group className="mb-3">
            <Form.Label>Current Password</Form.Label>
            <Form.Control type="password" name="current_password" value={formData.current_password} onChange={handleChange} required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>New Password</Form.Label>
            <Form.Control type="password" name="new_password" value={formData.new_password} onChange={handleChange} required />
          </Form.Group>
          <Button variant="warning" type="submit" className="w-100">Update Password</Button>
        </Form>
      </Card>
    </Container>
  );
}
