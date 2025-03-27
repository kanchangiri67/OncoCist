import { useState } from "react";
import { Navbar } from "../components/Navbar";
import { Container, Card, Form, Button, Spinner } from "react-bootstrap";

export default function Upload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ prediction: string; confidence: number } | null>(null);

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

  return (
    <div className="min-vh-100">
      <Navbar />
      <Container className="upload-container d-flex flex-column align-items-center">
        <Card className="card-custom p-4 w-50 text-center">
          <Card.Body>
            <Card.Title>Upload MRI Scan</Card.Title>
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Control type="file" onChange={handleFileChange} />
            </Form.Group>
            <Button onClick={handleUpload} disabled={loading} className="btn-custom w-100">
              {loading ? <Spinner animation="border" size="sm" /> : "Detect Tumor"}
            </Button>
          </Card.Body>
        </Card>
        {result && (
          <Card className="card-custom mt-4 p-4 w-50 text-center">
            <Card.Body>
              <Card.Title>Prediction Result</Card.Title>
              <p>{result.prediction}</p>
              <p>Confidence: {result.confidence}%</p>
            </Card.Body>
          </Card>
        )}
      </Container>
    </div>
  );
}
