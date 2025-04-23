import { useState } from "react";
import { Navbar } from "../components/Navbar";
import { Form, Button, Row, Col, Card, Container, Spinner } from "react-bootstrap";
import { useDropzone } from 'react-dropzone'; // Drag-and-drop

export default function Upload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null); // 👈 preview state
  const [loading, setLoading] = useState(false);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [doctorNotes, setDoctorNotes] = useState<string>(() => localStorage.getItem("doctorNotes") || "");
  const [patientInfo, setPatientInfo] = useState({ name: "", age: "", reports: "" });

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setSelectedFile(file);
        setPreview(URL.createObjectURL(file)); // 👈 generate preview
      }
    },
    accept: {
      'image/jpeg': ['.jpeg', '.jpg'],
      'image/png': ['.png'],
      'image/gif': ['.gif'],
    },
  });

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setResultImage(null); // 👈 Clear previous result before uploading
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResultImage(data.imageUrl);
    } catch (error) {
      console.error("Error uploading file", error);
    } finally {
      setLoading(false);
    }
  };

  const saveDoctorNotes = () => {
    localStorage.setItem("doctorNotes", doctorNotes);
    alert("Doctor's notes saved successfully!");
  };

  const clearDoctorNotes = () => {
    localStorage.removeItem("doctorNotes");
    setDoctorNotes("");
    alert("Doctor's notes cleared!");
  };

  const handlePatientChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setPatientInfo({ ...patientInfo, [e.target.name]: e.target.value });
  };

  const savePatientHistory = () => {
    const newPatientRecord = {
      name: patientInfo.name,
      age: patientInfo.age,
      reports: patientInfo.reports,
      resultImage: resultImage,
      doctorNotes: doctorNotes,
    };

    // Get existing patient records from localStorage
    const storedHistory = JSON.parse(localStorage.getItem("patientHistory") || "[]");
    storedHistory.push(newPatientRecord);

    // Save the updated patient history back to localStorage
    localStorage.setItem("patientHistory", JSON.stringify(storedHistory));

    alert("Patient history saved successfully!");
  };

  return (
    <div className="bg-light min-vh-100">
      <Navbar />
      <Container fluid="md" className="py-4">
        <Row>
          {/* Left Column */}
          <Col md={6} className="p-3">
            <div className="d-flex flex-column" style={{ height: "100%" }}>
              {/* Patient Demographics */}
              <Card className="mb-4 shadow-sm" style={{ flex: 1 }}>
                <Card.Body>
                  <Card.Title>Patient Demographics</Card.Title>
                  <Form>
                    <Form.Group className="mb-3">
                      <Form.Label>Name</Form.Label>
                      <Form.Control
                        type="text"
                        name="name"
                        value={patientInfo.name}
                        onChange={handlePatientChange}
                      />
                    </Form.Group>
                    <Form.Group className="mb-3">
                      <Form.Label>Age</Form.Label>
                      <Form.Control
                        type="text"
                        name="age"
                        value={patientInfo.age}
                        onChange={handlePatientChange}
                      />
                    </Form.Group>
                    <Form.Group>
                      <Form.Label>Previous Reports</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={2}
                        name="reports"
                        value={patientInfo.reports}
                        onChange={handlePatientChange}
                      />
                    </Form.Group>
                  </Form>
                </Card.Body>
              </Card>

              {/* Upload Section */}
              <Card className="shadow-sm" style={{ flex: 1 }}>
                <Card.Body>
                  <Card.Title className="mb-3">Upload MRI Scan</Card.Title>
                  <div
                    {...getRootProps()}
                    className="border rounded p-5 text-center mb-3 bg-white"
                    style={{
                      borderStyle: "dashed",
                      backgroundColor: "#f8f9fa",
                      cursor: "pointer",
                    }}
                  >
                    <input {...getInputProps()} />
                    <p className="text-muted">Drag & drop or click to browse to upload scan</p>
                  </div>

                  {/* 👇 Image Preview */}
                  {preview && (
                    <div className="mb-3 text-center">
                      <img
                        src={preview}
                        alt="Selected MRI"
                        className="img-fluid rounded border"
                        style={{ maxHeight: "200px" }}
                      />
                    </div>
                  )}

                  <div className="d-flex gap-2">
                    <Button
                      variant="primary"
                      onClick={handleUpload}
                      disabled={loading || !selectedFile}
                      className="w-50"
                    >
                      {loading ? (
                        <>
                          <Spinner animation="border" size="sm" /> Analyzing...
                        </>
                      ) : (
                        "Submit"
                      )}
                    </Button>
                    <Button
                      variant="outline-secondary"
                      onClick={() => {
                        setSelectedFile(null);
                        setPreview(null); // 👈 clear preview
                      }}
                      className="w-50"
                    >
                      Clear
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </div>
          </Col>

          {/* Right Column */}
          <Col md={6} className="p-3">
            <div className="d-flex flex-column" style={{ height: "100%" }}>
              {/* Output Section */}
              <Card className="mb-4 shadow-sm" style={{ flex: 1 }}>
                <Card.Body>
                  <Card.Title>Prediction Output</Card.Title>
                  <div
                    className="d-flex justify-content-center align-items-center border rounded"
                    style={{
                      width: "100%",
                      height: "350px", // 👈 Fixed square-like box
                      backgroundColor: "#f8f9fa",
                    }}
                  >
                    {loading ? (
                      <div className="text-center">
                        <Spinner animation="border" variant="primary" />
                        <p className="mt-2 text-muted">Processing...</p>
                      </div>
                    ) : resultImage ? (
                      <img
                        src={resultImage}
                        alt="Prediction Output"
                        className="img-fluid rounded border"
                        style={{ maxWidth: "100%", maxHeight: "100%" }}
                      />
                    ) : (
                      <p className="text-muted">Prediction result will be shown here.</p>
                    )}
                  </div>
                </Card.Body>
              </Card>

              {/* Doctor Notes */}
              <Card className="shadow-sm" style={{ flex: 1 }}>
                <Card.Body>
                  <Card.Title>Doctor's Notes</Card.Title>
                  <Form.Group className="mb-3">
                    <Form.Control
                      as="textarea"
                      rows={4}
                      value={doctorNotes}
                      onChange={(e) => setDoctorNotes(e.target.value)}
                      placeholder="Enter doctor's observations..."
                    />
                  </Form.Group>
                  <div className="d-flex gap-2">
                    <Button variant="success" className="w-50" onClick={saveDoctorNotes}>
                      Save Notes
                    </Button>
                    <Button variant="danger" className="w-50" onClick={clearDoctorNotes}>
                      Clear Notes
                    </Button>
                  </div>
                  <Button variant="primary" className="w-100 mt-3" onClick={savePatientHistory}>
                    Save Patient History
                  </Button>
                </Card.Body>
              </Card>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
