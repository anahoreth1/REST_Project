import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// for tokens
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  const authFreeUrls = ["/users/", "/users/login/"];

  const isAuthFree = authFreeUrls.includes(config.url);

  config.headers = config.headers || {};
  if (!isAuthFree && token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;
