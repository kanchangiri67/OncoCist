// src/services/AuthService.ts
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/auth'; 

const login = async (email: string, password: string): Promise<{ accessToken: string; refreshToken: string }> => {
  const response = await axios.post(`${API_URL}/login`, { email, password });
  return response.data;
};

const AuthService = {
  login,
};

export default AuthService;
