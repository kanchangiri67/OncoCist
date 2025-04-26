import React from "react";
import { Navbar } from "../components/Navbar";
import { Link } from "react-router-dom";
import { Button, Container } from "react-bootstrap";

const Home: React.FC = () => {
  return (
    <div className="home-container">
      {/* Background Video */}
      <video className="video-background" autoPlay muted loop playsInline>
        <source src="/src/assets/159049-818026306_small.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div className="home-overlay"></div>

      <Navbar />

      <Container className="home-content">
        <h1>Welcome to OncoCist</h1>
        <p>
          Use advanced technology to detect and analyze brain tumors efficiently.
        </p>
        <Link to="/upload">
          <Button className="btn-custom btn-lg mt-3">Get Started</Button>
        </Link>
      </Container>
    </div>
  );
};

export default Home;
