import React from 'react';
import { Navbar } from '../components/Navbar'; 
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="home-container relative min-h-screen">
      {/* Background video */}
      <video
        className="video-background absolute inset-0 w-full h-full object-cover"
        autoPlay
        muted
        loop
        playsInline
      >
         <source src="/src/assets/159049-818026306_small.mp4" type="video/mp4" />
      </video>

      <Navbar />

      <div className="home-section absolute inset-0 flex flex-col justify-center items-center text-center text-white bg-black bg-opacity-50">
        <h1 className="text-5xl font-bold">Welcome to OncoCist</h1>
        <p className="mt-4 text-xl">Use advanced technology to detect and analyze brain tumors efficiently.</p>
         <Link to="/upload"> {/* Link to Upload page */}
          <button className="bg-blue-500 text-white py-2 px-6 rounded mt-6 hover:bg-blue-700">
            Get Started
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Home;
