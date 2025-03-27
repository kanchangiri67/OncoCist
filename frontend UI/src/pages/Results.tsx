import { Navbar } from "../components/Navbar";
import { Container, Card } from "react-bootstrap";
import { useEffect, useState } from "react";

export default function Results() {
  const [doctorNotes, setDoctorNotes] = useState("");

  useEffect(() => {
    const savedNotes = localStorage.getItem("doctorNotes");
    if (savedNotes) {
      setDoctorNotes(savedNotes);
    }
  }, []);

  return (
    <div className="min-vh-100">
      <Navbar />
      <Container className="d-flex flex-column align-items-center py-5">
        <Card className="card-custom p-4 w-50 text-center">
          <Card.Body>
            <Card.Title>Previous Results</Card.Title>
            <p>No past results found. Please upload an MRI scan.</p>
            {doctorNotes && (
              <div className="mt-3">
                <h5>Doctor's Notes</h5>
                <p>{doctorNotes}</p>
              </div>
            )}
          </Card.Body>
        </Card>
      </Container>
    </div>
  );
}
