/**
 * Axios instance configured for the Movie Explorer API.
 *
 * baseURL is /api so that:
 *  - In development (vite dev server), the proxy in vite.config.ts forwards
 *    /api → http://localhost:8000/api.
 *  - In production (Docker), nginx proxies /api → backend:8000/api.
 */
import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default client
