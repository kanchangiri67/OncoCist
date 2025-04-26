import { Link, useNavigate } from "react-router-dom";
import { Navbar as BSNavbar, Nav, Container, Button } from "react-bootstrap";

export const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("access_token");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <BSNavbar expand="lg" bg="light" className="shadow-sm mb-3">
      <Container>
        <BSNavbar.Brand as={Link} to="/home" className="fw-bold text-primary">
          OncoCist
        </BSNavbar.Brand>
        <BSNavbar.Toggle aria-controls="main-navbar" />
        <BSNavbar.Collapse id="main-navbar">
          <Nav className="ms-auto align-items-center">
            <Nav.Link as={Link} to="/home">
              Home
            </Nav.Link>
            <Nav.Link as={Link} to="/upload">
              Upload
            </Nav.Link>
            <Nav.Link as={Link} to="/results">
              History
            </Nav.Link>
            <Nav.Link as={Link} to="/about">
              About
            </Nav.Link>
            {isLoggedIn && (
              <Button
                variant="outline-danger"
                size="sm"
                className="ms-3"
                onClick={handleLogout}
              >
                Logout
              </Button>
            )}
          </Nav>
        </BSNavbar.Collapse>
      </Container>
    </BSNavbar>
  );
};
