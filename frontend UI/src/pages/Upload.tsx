import { useState } from "react";
import { Navbar } from "../components/Navbar";
import {
  Form,
  Button,
  Row,
  Col,
  Card,
  Container,
  Spinner,
} from "react-bootstrap";
import { useDropzone } from "react-dropzone";

export default function Upload() {
  const today = new Date().toISOString().split("T")[0];

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [tumorType, setTumorType] = useState<string>("");
  const [doctorNotes, setDoctorNotes] = useState<string>(() =>
    localStorage.getItem("doctorNotes") || ""
  );
  const [patientInfo, setPatientInfo] = useState({
    name: "",
    age: "",
    sex: "",
    scan_date: today,
  });

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setSelectedFile(file);
        setPreview(URL.createObjectURL(file));
      }
    },
    accept: {
      "image/jpeg": [".jpeg", ".jpg"],
      "image/png": [".png"],
    },
  });

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setResultImage(null);
    setTumorType("");

    const formData = new FormData();
    formData.append("files", selectedFile);
    formData.append("patient_name", patientInfo.name);
    formData.append("age", String(parseInt(patientInfo.age)));
    formData.append("sex", patientInfo.sex);
    formData.append("scan_date", patientInfo.scan_date);
    formData.append("doctor_notes", doctorNotes);

    let token = localStorage.getItem("access_token");
    if (!token) {
      const auth = JSON.parse(localStorage.getItem("auth") || "{}");
      token = auth.access_token;
    }

    if (!token) {
      alert("You are not logged in. Please log in to upload.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/mri/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        const msg = Array.isArray(data.detail)
          ? data.detail.map((d) => `${d.loc.join(".")}: ${d.msg}`).join("\n")
          : data.detail || "Upload failed.";
        alert(`Upload failed:\n${msg}`);
        return;
      }

      const scanId = data[0]?.id;
      if (scanId) {
        const predictionRes = await fetch(
          `http://localhost:8000/predict/${scanId}`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const predictionData = await predictionRes.json();

        if (predictionRes.ok) {
          const filename = predictionData.overlay_image_path.split("/").pop();
          setResultImage(`http://localhost:8000/predictions/${filename}`);
          setTumorType(predictionData.tumor_type);
        } else {
          alert("Prediction failed.");
        }
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handlePatientChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    setPatientInfo({ ...patientInfo, [e.target.name]: e.target.value });
  };

  return (
    <div className="bg-light min-vh-100">
      <Navbar />
      <Container fluid="md" className="py-4">
        <Row>
          <Col md={6} className="p-3">
            <div className="d-flex flex-column" style={{ height: "100%" }}>
              <Card className="mb-4 shadow-sm" style={{ flex: 1 }}>
                <Card.Body>
                  <Card.Title>Patient Demographics</Card.Title>
                  <Form>
                    <Form.Group className="mb-2">
                      <Form.Label>Name</Form.Label>
                      <Form.Control
                        type="text"
                        name="name"
                        value={patientInfo.name}
                        onChange={handlePatientChange}
                      />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Age</Form.Label>
                      <Form.Control
                        type="text"
                        name="age"
                        value={patientInfo.age}
                        onChange={handlePatientChange}
                      />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Sex</Form.Label>
                      <Form.Select
                        name="sex"
                        value={patientInfo.sex}
                        onChange={handlePatientChange}
                      >
                        <option value="">-- Select --</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                      </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Scan Date</Form.Label>
                      <Form.Control
                        type="date"
                        name="scan_date"
                        value={patientInfo.scan_date}
                        onChange={handlePatientChange}
                      />
                    </Form.Group>
                  </Form>
                </Card.Body>
              </Card>

              <Card className="shadow-sm" style={{ flex: 1 }}>
                <Card.Body>
                  <Card.Title className="mb-3">Upload MRI Scan</Card.Title>
                  <div
                    {...getRootProps()}
                    className="border rounded p-5 text-center mb-3 bg-white"
                    style={{ borderStyle: "dashed", backgroundColor: "#f8f9fa" }}
                  >
                    <input {...getInputProps()} />
                    <p className="text-muted">Drag & drop or click to upload</p>
                  </div>
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
                        setPreview(null);
                        setResultImage(null);
                        setTumorType("");
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

          <Col md={6} className="p-3">
            <div className="d-flex flex-column" style={{ height: "100%" }}>
              <Card className="mb-4 shadow-sm" style={{ flex: 1 }}>
                <Card.Body>
                  <Card.Title>Prediction Output</Card.Title>
                  <div
                    className="d-flex justify-content-center align-items-center border rounded mb-3"
                    style={{ width: "100%", height: "350px", backgroundColor: "#f8f9fa" }}
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

                  {tumorType && (
                    <Form.Group className="mt-3">
                      <Form.Label>Predicted Tumor Type</Form.Label>
                      <Form.Control type="text" value={tumorType} readOnly />
                    </Form.Group>
                  )}
                </Card.Body>
              </Card>

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
                    <Button
                      variant="success"
                      className="w-50"
                      onClick={() => {
                        localStorage.setItem("doctorNotes", doctorNotes);
                        alert("Doctor's notes saved successfully!");
                      }}
                    >
                      Save Notes
                    </Button>
                    <Button
                      variant="danger"
                      className="w-50"
                      onClick={() => {
                        localStorage.removeItem("doctorNotes");
                        setDoctorNotes("");
                        alert("Doctor's notes cleared!");
                      }}
                    >
                      Clear Notes
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
