import axios from 'axios'; import { useAuth } from '../store/auth.js';
export const api=axios.create({baseURL:import.meta.env.VITE_API_BASE_URL||'http://localhost:8000/api'});
api.interceptors.request.use(c=>{const t=useAuth.getState().token;if(t)c.headers.Authorization=`Bearer ${t}`;return c});
api.interceptors.response.use(r=>r,e=>{if(e.response?.status===401)useAuth.getState().logout();return Promise.reject(e)});
