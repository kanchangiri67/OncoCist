import { Navbar } from "../components/Navbar";
import { Container, Card, } from "react-bootstrap";

export default function About() {
  return (
    <div className="min-vh-100">
      <Navbar />
      <Container className="d-flex flex-column align-items-center py-5">
        <Card className="card-custom p-4 w-75 text-center">
          <Card.Body>
            <Card.Title>About OncoCist</Card.Title>
            <p>
              OncoCist is an AI-powered brain tumor detection system that assists medical professionals
              in diagnosing tumors with high accuracy. Our deep learning model analyzes Images and
              provides precise predictions, helping doctors make informed decisions faster.
            </p>
          </Card.Body>
        </Card>
      </Container>
    </div>
  );
}
