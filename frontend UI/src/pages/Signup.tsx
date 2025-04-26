import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container, Alert } from "react-bootstrap";
import axios from "axios";

export default function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    full_name: "",
    position: "",
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/auth/signup", formData, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      alert("Signup successful! You can now log in.");
      navigate("/");
    } catch (err: any) {
      console.error("Signup error:", err.response?.data || err);
      const detail =
        err.response?.data?.error || err.response?.data?.detail || "Signup failed.";
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
        <Card style={{ width: "100%", maxWidth: "450px" }} className="p-4 shadow-sm">
          <Card.Title className="text-center mb-3">Sign Up</Card.Title>

          {error && <Alert variant="danger">{error}</Alert>}

          <Form onSubmit={handleSignup}>
            <Form.Group className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Position</Form.Label>
              <Form.Select
                value={formData.position}
                onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                required
              >
                <option value="">-- Select Position --</option>
                <option value="Doctor">Doctor</option>
                <option value="Nurse">Nurse</option>
                <option value="Radiologist">Radiologist</option>
                <option value="Surgeon">Surgeon</option>
                <option value="Pathologist">Pathologist</option>
                <option value="Oncologist">Oncologist</option>
                <option value="Medical Student">Medical Student</option>
                <option value="Researcher">Researcher</option>
                <option value="Technician">Technician</option>
                <option value="Other">Other</option>
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
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

            <Button variant="success" type="submit" className="w-100">
              Sign Up
            </Button>

            <Button
              variant="link"
              className="w-100 mt-2"
              onClick={() => navigate("/")}
            >
              Already have an account? Login
            </Button>
          </Form>
        </Card>
      </Container>
    </>
  );
}
