import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container } from "react-bootstrap";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate user signup
    localStorage.setItem("auth", "true");
    navigate("/upload");
  };

  return (
    <Container className="d-flex justify-content-center align-items-center min-vh-100">
      <Card style={{ width: "100%", maxWidth: "400px" }} className="p-4 shadow-sm">
        <Card.Title className="text-center mb-3">Sign Up</Card.Title>
        <Form onSubmit={handleSignup}>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </Form.Group>
          <Button variant="success" type="submit" className="w-100">Sign Up</Button>
          <Button variant="link" className="w-100 mt-2" onClick={() => navigate("/")}>
            Already have an account? Login
          </Button>
        </Form>
      </Card>
    </Container>
  );
}
