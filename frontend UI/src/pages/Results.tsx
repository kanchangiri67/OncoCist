import { Navbar } from "../components/Navbar";
import { Container, Card, Row, Col, Button, Form, Modal } from "react-bootstrap";
import { useEffect, useState } from "react";

export default function Results() {
  const [patientHistory, setPatientHistory] = useState<any[]>([]);
  const [fullHistory, setFullHistory] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [patientToDelete, setPatientToDelete] = useState<number | null>(null);
  const [patients, setPatients] = useState<any[]>([]);
  const [selectedPatientName, setSelectedPatientName] = useState<string | null>(null);

  useEffect(() => {
    fetchAllHistory();
    fetchPatients();
  }, []);

  const fetchAllHistory = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("http://localhost:8000/history/user/all", {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await res.json();
      const historyArray = Array.isArray(data.scans) ? data.scans : [];
      setFullHistory(historyArray);
      setPatientHistory(historyArray);
    } catch (err) {
      console.error("Error fetching history:", err);
    }
  };

  const fetchPatients = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("http://localhost:8000/history/user/patients", {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await res.json();

      const patientList = Array.isArray(data)
        ? data
        : Array.isArray(data.patients)
        ? data.patients
        : [];

      const uniquePatients = Object.values(
        patientList.reduce((acc: any, patient: any) => {
          const name = patient.patient_name || patient.name || "Unnamed";
          if (!acc[name]) acc[name] = patient;
          return acc;
        }, {})
      );

      setPatients(uniquePatients);
    } catch (err) {
      console.error("Error fetching patients:", err);
      setPatients([]);
    }
  };

  const handlePatientSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedName = e.target.value;
    setSelectedPatientName(selectedName);

    if (!selectedName) {
      setPatientHistory(fullHistory);
    } else {
      const filtered = fullHistory.filter(
        (scan) => scan.patient?.patient_name?.toLowerCase() === selectedName.toLowerCase()
      );
      setPatientHistory(filtered);
    }
  };

  const filteredHistory = patientHistory.filter((scan) =>
    (scan.patient?.patient_name || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeletePatient = (index: number) => {
    setPatientToDelete(index);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    if (patientToDelete !== null) {
      const scanId = patientHistory[patientToDelete].scan_id;
      const token = localStorage.getItem("access_token");

      try {
        const res = await fetch(`http://localhost:8000/history/delete/${scanId}`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) throw new Error("Failed to delete");
        const updated = patientHistory.filter((_, i) => i !== patientToDelete);
        const updatedFull = fullHistory.filter((scan) => scan.scan_id !== scanId);
        setPatientHistory(updated);
        setFullHistory(updatedFull);
      } catch (err) {
        alert("Failed to delete scan.");
        console.error(err);
      } finally {
        setShowDeleteModal(false);
        setPatientToDelete(null);
      }
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

            <Row className="mb-3">
              <Col md={6}>
                <Form.Control
                  type="text"
                  placeholder="Search by Patient Name"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </Col>
              <Col md={6}>
                <Form.Select onChange={handlePatientSelect} value={selectedPatientName || ""}>
                  <option value="">All Patients</option>
                  {patients.map((patient: any) => (
                    <option key={patient.patient_name} value={patient.patient_name}>
                      {patient.patient_name}
                    </option>
                  ))}
                </Form.Select>
              </Col>
            </Row>

            {filteredHistory.length === 0 ? (
              <p>No patient history available.</p>
            ) : (
              Object.entries(
                filteredHistory.reduce((grouped: any, scan: any) => {
                  const name = scan.patient?.patient_name || "Unknown";
                  if (!grouped[name]) grouped[name] = [];
                  grouped[name].push(scan);
                  return grouped;
                }, {})
              ).map(([patientName, scans]: [string, any[]], index) => {
                const patient = scans[0].patient;

                return (
                  <Col key={patientName + index} sm={12} className="mb-5">
                    <Card className="shadow border-light">
                      <Card.Body>
                        <h5 className="text-primary mb-3">{patientName}</h5>
                        <p><strong>Sex:</strong> {patient?.patient_sex || "N/A"}</p>
                        <p><strong>Age:</strong> {patient?.patient_age || "N/A"}</p>

                        <Row>
                          {scans.map((scan, i) => (
                            <Col key={scan.scan_id || i} sm={12} md={6} lg={4} className="mb-4">
                              <Card className="border-light">
                                <Card.Body>
                                  <p><strong>Scan Date:</strong> {scan.uploaded_at ? new Date(scan.uploaded_at).toLocaleString() : "N/A"}</p>
                                  <p><strong>Prediction Status:</strong> {scan.prediction_status || "Pending"}</p>
                                  <p><strong>Tumor Type:</strong> {scan.tumor_type || "N/A"}</p>
                                  {scan.doctor_notes && (
                                    <div className="mt-2 p-2 border rounded bg-light">
                                      <p className="mb-1"><strong>Doctor Notes:</strong></p>
                                      <p className="mb-0" style={{ whiteSpace: "pre-wrap" }}>{scan.doctor_notes}</p>
                                    </div>
                                  )}

                                  <div
                                    className="d-flex justify-content-center align-items-center border rounded mb-3 mt-3"
                                    style={{ width: "100%", height: "180px", backgroundColor: "#f8f9fa" }}
                                  >
                                    <img
                                      src={`http://localhost:8000/${scan.prediction_result_path || scan.file_path}`}
                                      alt="Scan Result"
                                      className="img-fluid rounded"
                                      style={{ maxWidth: "100%", maxHeight: "100%" }}
                                    />
                                  </div>

                                  <Button
                                    variant="danger"
                                    onClick={() => handleDeletePatient(patientHistory.indexOf(scan))}
                                    className="w-100"
                                  >
                                    Remove Scan
                                  </Button>
                                </Card.Body>
                              </Card>
                            </Col>
                          ))}
                        </Row>
                      </Card.Body>
                    </Card>
                  </Col>
                );
              })
            )}
          </Card.Body>
        </Card>
      </Container>

      <Modal show={showDeleteModal} onHide={cancelDelete}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Are you sure you want to delete this scan?</p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={cancelDelete}>Cancel</Button>
          <Button variant="danger" onClick={confirmDelete}>Yes, Delete</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
