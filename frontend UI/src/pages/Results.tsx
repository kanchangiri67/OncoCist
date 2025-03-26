import { Navbar } from "../components/Navbar";

export default function Results() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="container mx-auto py-10 text-center">
        <h2 className="text-3xl font-bold">Previous Results</h2>
        <p className="text-gray-600 mt-4">No past results found. Please upload an MRI scan.</p>
      </div>
    </div>
  );
}
