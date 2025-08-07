import React, { createContext, useContext, useState, useEffect } from 'react';
import toast from 'react-hot-toast';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (userData: RegisterData) => Promise<boolean>;
  logout: () => void;
  isLoading: boolean;
}

interface RegisterData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  age: number;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// API Helper function
async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add auth token if it exists
  const token = localStorage.getItem('token');
  if (token && defaultOptions.headers) {
    (defaultOptions.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, defaultOptions);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP error! status: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is logged in on app start
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token and get user info
      apiRequest('/auth/me')
        .then(response => {
          setUser(response);
        })
        .catch(() => {
          // Token is invalid, remove it
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        })
        .finally(() => {
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // OAuth2 login format
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await fetch(`${API_BASE_URL}/auth/token`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      const { access_token } = data;

      // Store token
      localStorage.setItem('token', access_token);

      // Get user info
      const userResponse = await apiRequest('/auth/me');
      setUser(userResponse);
      localStorage.setItem('user', JSON.stringify(userResponse));

      toast.success('Welcome back!');
      return true;
    } catch (error: any) {
      const message = error.message || 'Login failed';
      toast.error(message);
      return false;
    }
  };

  const register = async (userData: RegisterData): Promise<boolean> => {
    try {
      await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      });

      toast.success('Account created successfully! Please log in.');
      return true;
    } catch (error: any) {
      const message = error.message || 'Registration failed';
      toast.error(message);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    toast.success('Logged out successfully');
  };

  const value = {
    user,
    login,
    register,
    logout,
    isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}