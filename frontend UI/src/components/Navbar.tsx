import { Link } from "react-router-dom";
import { Navbar as BSNavbar, Nav, Container } from "react-bootstrap";

export const Navbar = () => {
  return (
    <BSNavbar expand="lg" className="navbar">
      <Container>
        <BSNavbar.Brand as={Link} to="/" className="navbar-brand">
          OncoCist
        </BSNavbar.Brand>
        <BSNavbar.Toggle aria-controls="basic-navbar-nav" />
        <BSNavbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/" className="nav-link">
              Home
            </Nav.Link>
            <Nav.Link as={Link} to="/upload" className="nav-link">
              Upload
            </Nav.Link>
            <Nav.Link as={Link} to="/results" className="nav-link">
              History
            </Nav.Link>
            <Nav.Link as={Link} to="/about" className="nav-link">
              About
            </Nav.Link>
          </Nav>
        </BSNavbar.Collapse>
      </Container>
    </BSNavbar>
  );
};
