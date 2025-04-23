import { Link, useNavigate } from "react-router-dom";
import { Navbar as BSNavbar, Nav, Container, Button } from "react-bootstrap";

export const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = localStorage.getItem("auth") === "true";

  const handleLogout = () => {
    localStorage.removeItem("auth");
    navigate("/");
  };

  return (
    <BSNavbar expand="lg" className="navbar">
      <Container>
        <BSNavbar.Brand as={Link} to="/" className="navbar-brand">
          OncoCist
        </BSNavbar.Brand>
        <BSNavbar.Toggle aria-controls="basic-navbar-nav" />
        <BSNavbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto align-items-center">
            <Nav.Link as={Link} to="/home" className="nav-link">
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
            {isLoggedIn && (
              <Button variant="outline-danger" size="sm" className="ms-3" onClick={handleLogout}>
                Logout
              </Button>
            )}
          </Nav>
        </BSNavbar.Collapse>
      </Container>
    </BSNavbar>
  );
};
