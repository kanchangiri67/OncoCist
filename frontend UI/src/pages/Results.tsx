import { Navbar } from "../components/Navbar";
import { Container, Card, Row, Col, Button, Form, Modal } from "react-bootstrap";
import { useEffect, useState } from "react";

export default function Results() {
  const [patientHistory, setPatientHistory] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [patientToDelete, setPatientToDelete] = useState<number | null>(null);

  useEffect(() => {
    const history = JSON.parse(localStorage.getItem("patientHistory") || "[]");
    setPatientHistory(history);
  }, []);

  // Filter patient history based on the search term
  const filteredHistory = patientHistory.filter((patient) =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeletePatient = (index: number) => {
    setPatientToDelete(index);
    setShowDeleteModal(true);
  };

  const confirmDelete = () => {
    if (patientToDelete !== null) {
      const updatedHistory = patientHistory.filter((_, index) => index !== patientToDelete);
      localStorage.setItem("patientHistory", JSON.stringify(updatedHistory));
      setPatientHistory(updatedHistory);
      setShowDeleteModal(false);
      setPatientToDelete(null);
    }
  };

  const cancelDelete = () => {
    setShowDeleteModal(false);
    setPatientToDelete(null);
  };

  return (
    <div className="min-vh-100 bg-light">
      <Navbar />
      <Container className="py-5">
        <Card className="card-custom p-4 w-100">
          <Card.Body>
            <Card.Title>Patient History</Card.Title>

            {/* Search Bar */}
            <Form className="mb-3">
              <Form.Control
                type="text"
                placeholder="Search by Patient Name"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </Form>

            {filteredHistory.length === 0 ? (
              <p>No patient history available. Please upload MRI scans.</p>
            ) : (
              <Row>
                {filteredHistory.map((patient, index) => (
                  <Col key={index} sm={12} md={6} lg={4} className="mb-4">
                    <Card className="shadow-sm border-light">
                      <Card.Body>
                        <Card.Title className="text-primary">{patient.name}</Card.Title>
                        <p><strong>Age:</strong> {patient.age} years</p>
                        <p><strong>Reports:</strong> {patient.reports}</p>

                        <div
                          className="d-flex justify-content-center align-items-center border rounded mb-3"
                          style={{
                            width: "100%",
                            height: "200px",
                            backgroundColor: "#f8f9fa",
                          }}
                        >
                          <img
                            src={patient.resultImage}
                            alt="Result"
                            className="img-fluid rounded"
                            style={{ maxWidth: "100%", maxHeight: "100%" }}
                          />
                        </div>

                        <p><strong>Doctor's Notes:</strong></p>
                        <p>{patient.doctorNotes}</p>

                        {/* Remove Patient Button */}
                        <Button
                          variant="danger"
                          onClick={() => handleDeletePatient(index)}
                          className="w-100 mt-3"
                        >
                          Remove History
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                ))}
              </Row>
            )}
          </Card.Body>
        </Card>
      </Container>

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={cancelDelete}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Are you sure you want to delete this patient's record?</p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={cancelDelete}>
            Cancel
          </Button>
          <Button variant="danger" onClick={confirmDelete}>
            Yes, Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
