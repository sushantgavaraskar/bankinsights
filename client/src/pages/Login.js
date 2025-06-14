import React, { useState } from "react";
import { Button, Card, Container, Form, Alert } from "react-bootstrap";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FaLock } from "react-icons/fa";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(formData.email, formData.password);
      navigate("/dashboard");
    } catch {
      setError("Invalid credentials. Please try again.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: "90vh" }}>
      <Card className="p-4 shadow-sm" style={{ minWidth: "320px", maxWidth: "400px", width: "100%" }}>
        <div className="text-center mb-3">
          <FaLock size={36} color="#008080" />
          <h4 className="mt-2">Login to TransactIQ</h4>
        </div>
        <Form onSubmit={handleSubmit}>
          {error && <Alert variant="danger">{error}</Alert>}
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" name="email" value={formData.email} onChange={handleChange} required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" name="password" value={formData.password} onChange={handleChange} required />
          </Form.Group>
          <Button type="submit" className="w-100" style={{ backgroundColor: "#008080", border: "none" }}>
            Login
          </Button>
        </Form>

        <div className="text-center mt-3">
          <Link to="/change-password" style={{ color: "#008080", fontSize: "0.9rem" }}>
            Forgot Password?
          </Link>
          <br />
          <span style={{ fontSize: "0.9rem" }}>
            Don’t have an account?{" "}
            <Link to="/register" style={{ color: "#008080" }}>
              Register
            </Link>
          </span>
        </div>
      </Card>
    </Container>
  );
}
