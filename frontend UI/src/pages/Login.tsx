import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container, Alert } from "react-bootstrap";
import axios from "axios";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await axios.post("http://localhost:8000/auth/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token, refresh_token } = response.data;

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);

      navigate("/home");
    } catch (err: any) {
      console.error("Login error:", err.response?.data || err);

      const detail =
        err.response?.data?.error ||
        err.response?.data?.detail ||
        "Login failed. Please try again.";

      setError(detail);
    }
  };

  return (
    <>
      <div className="border-bottom py-3">
        <div className="container">
          <div className="d-flex justify-content-center">
            <h4 className="fw-bold text-primary m-0">OncoCist</h4>
          </div>
        </div>
      </div>

      <Container
        fluid
        className="d-flex flex-column justify-content-center align-items-center"
        style={{ minHeight: "100vh" }}
      >
        <Card style={{ width: "100%", maxWidth: "400px" }} className="p-4 shadow-sm">
          <Card.Title className="text-center mb-3">Login</Card.Title>

          {error && <Alert variant="danger">{error}</Alert>}

          <Form onSubmit={handleLogin}>
            <Form.Group className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <Form.Check
                type="checkbox"
                label="Show Password"
                checked={showPassword}
                onChange={() => setShowPassword((prev) => !prev)}
                className="mt-2"
              />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100">
              Login
            </Button>

            <Button
              variant="link"
              className="w-100 mt-2"
              onClick={() => navigate("/signup")}
            >
              Don&apos;t have an account? Sign Up
            </Button>
          </Form>
        </Card>
      </Container>
    </>
  );
}
