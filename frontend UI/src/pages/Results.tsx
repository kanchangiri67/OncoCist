import { Navbar } from "../components/Navbar";
import { Container, Card } from "react-bootstrap";

export default function Results() {
  return (
    <div className="min-vh-100">
      <Navbar />
      <Container className="d-flex flex-column align-items-center py-5">
        <Card className="card-custom p-4 w-50 text-center">
          <Card.Body>
            <Card.Title>Previous Results</Card.Title>
            <p>No past results found. Please upload an MRI scan.</p>
          </Card.Body>
        </Card>
      </Container>
    </div>
  );
}
