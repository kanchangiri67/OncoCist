import { Link } from "react-router-dom";

export const Navbar = () => {
  return (
    <nav className="navbar-container">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="navbar-title">OncoCist</h1>
        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/upload" className="nav-link">Upload</Link>
          <Link to="/results" className="nav-link">History</Link>
        </div>
      </div>
    </nav>
  );
};
