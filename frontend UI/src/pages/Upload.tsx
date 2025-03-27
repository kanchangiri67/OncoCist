import { useState } from "react";
import { Navbar } from "../components/Navbar";
import { Form, Button, Card, Container } from "react-bootstrap";

export default function Upload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ prediction: string; confidence: number } | null>(null);
  const [doctorNotes, setDoctorNotes] = useState<string>(() => {
    return localStorage.getItem("doctorNotes") || "";
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data);
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

  return (
    <div className="min-vh-100 bg-light">
      <Navbar />
      <Container className="py-5 d-flex flex-column align-items-center">
        <Card className="shadow-lg p-4 text-center" style={{ maxWidth: "500px", width: "100%" }}>
          <h2 className="text-primary">Upload MRI Scan</h2>
          <Form.Group>
            <Form.Control type="file" onChange={handleFileChange} className="my-3" />
          </Form.Group>
          <Button onClick={handleUpload} disabled={loading} className="btn btn-success w-100">
            {loading ? "Analyzing..." : "Detect Tumor"}
          </Button>
        </Card>

        {result && (
          <Card className="shadow-lg p-4 mt-4 text-center" style={{ maxWidth: "500px", width: "100%" }}>
            <h3 className="text-danger">Prediction Result</h3>
            <p className="fw-bold text-dark">{result.prediction}</p>
            <p className="text-muted">Confidence: {result.confidence}%</p>
          </Card>
        )}

        {/* Doctor's Notes Section */}
        <Card className="shadow-lg p-4 mt-4" style={{ maxWidth: "500px", width: "100%" }}>
          <h4 className="text-info">Doctor's Notes</h4>
          <Form.Group>
            <Form.Control
              as="textarea"
              rows={3}
              value={doctorNotes}
              onChange={(e) => setDoctorNotes(e.target.value)}
              placeholder="Enter doctor's observations..."
            />
          </Form.Group>
          <Button className="btn btn-secondary mt-3 w-100" onClick={saveDoctorNotes}>
            Save Notes
          </Button>
          <Button className="btn btn-danger mt-2 w-100" onClick={clearDoctorNotes}>
            Clear Notes
          </Button>
        </Card>
      </Container>
    </div>
  );
}
