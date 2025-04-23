import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Results from "./pages/Results";
import About from "./pages/About";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

const isAuthenticated = () => localStorage.getItem("auth") === "true";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={isAuthenticated() ? <Home /> : <Navigate to="/" />} />
        <Route path="/upload" element={isAuthenticated() ? <Upload /> : <Navigate to="/" />} />
        <Route path="/results" element={isAuthenticated() ? <Results /> : <Navigate to="/" />} />
        <Route path="/about" element={isAuthenticated() ? <About /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
