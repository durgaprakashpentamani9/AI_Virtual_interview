import axios from 'axios';
import { useAuth } from '../store/auth.js';

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL;
const baseURL = (rawBaseUrl && rawBaseUrl.trim()) ? rawBaseUrl.replace(/\/+$/, '') : '/api';

export const api = axios.create({ baseURL });
api.interceptors.request.use((c) => {
  const t = useAuth.getState().token;
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});
api.interceptors.response.use(
  (r) => r,
  (e) => {
    if (e.response?.status === 401) useAuth.getState().logout();
    return Promise.reject(e);
  }
);
