import { useState } from "react";
import { Navbar } from "../components/Navbar";

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
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="container mx-auto py-10 flex flex-col items-center">
        <div className="bg-white p-6 shadow-lg rounded-md w-96 text-center">
          <h2 className="text-xl font-semibold mb-4">Upload MRI Scan</h2>
          <input type="file" onChange={handleFileChange} className="mb-4" />
          <button
            onClick={handleUpload}
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded-md"
          >
            {loading ? "Analyzing..." : "Detect Tumor"}
          </button>
        </div>
        {result && (
          <div className="mt-6 p-4 bg-white shadow-md rounded-md">
            <h3 className="text-lg font-bold">Prediction Result</h3>
            <p className="text-gray-700">{result.prediction}</p>
            <p className="text-gray-500">Confidence: {result.confidence}%</p>
          </div>
        )}
      </div>
    </div>
  );
}
