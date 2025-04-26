import { Navbar } from "../components/Navbar";
import { Container, Card, Row, Col, Form, Button } from "react-bootstrap";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function About() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submitted:", form);
    alert("Thank you! We’ll get back to you soon.");
    setForm({ name: "", email: "", message: "" });
  };

  return (
    <div className="min-vh-100 bg-light">
      <Navbar />

      {/* Hero section */}
      <Container className="text-center py-5">
        <h1 className="fw-bold mb-3">OncoCist</h1>
        <p className="lead text-muted w-75 mx-auto">
          AI-powered brain tumor detection to assist healthcare professionals with faster and more accurate diagnoses.
        </p>
        <Button variant="primary" size="lg" className="mt-3" onClick={() => navigate("/upload")}>
          Explore the System
        </Button>
      </Container>

      {/* About body */}
      <Container className="py-5 bg-white">
        <Card className="shadow-sm p-4">
          <Card.Body>
            <Card.Title className="fs-4">Why OncoCist Exists</Card.Title>
            <p>
              Our mission is to support clinicians and patients with timely, AI-driven analysis of MRI brain scans.
              We aim to bridge the gap between radiology and real-time insights using cutting-edge deep learning.
              OncoCist empowers early detection, improves diagnostic accuracy, and contributes to better patient outcomes.
            </p>
            <p>
              Built by a passionate team of engineers, OncoCist is a project with impact at its core.
              We believe that technology should augment human decisions, not replace them — and our tools reflect that philosophy.
            </p>
          </Card.Body>
        </Card>
      </Container>

      {/* Contact form */}
      <Container className="py-5 bg-light">
        <Card className="p-4 shadow-sm w-100">
          <Card.Body>
            <Card.Title className="text-center fs-4 mb-4">Contact Us</Card.Title>
            <Form onSubmit={handleSubmit}>
              <Row className="mb-3">
                <Col md={6}>
                  <Form.Group controlId="formName">
                    <Form.Label>Full Name</Form.Label>
                    <Form.Control
                      type="text"
                      placeholder="Enter your name"
                      name="name"
                      value={form.name}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group controlId="formEmail">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                      type="email"
                      placeholder="you@example.com"
                      name="email"
                      value={form.email}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
              </Row>
              <Form.Group className="mb-3" controlId="formMessage">
                <Form.Label>Question or Comment</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={4}
                  name="message"
                  value={form.message}
                  onChange={handleChange}
                  placeholder="Describe your issue or ask a question..."
                  required
                />
              </Form.Group>
              <div className="text-center">
                <Button variant="success" type="submit">Submit</Button>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </Container>
    </div>
  );
}
