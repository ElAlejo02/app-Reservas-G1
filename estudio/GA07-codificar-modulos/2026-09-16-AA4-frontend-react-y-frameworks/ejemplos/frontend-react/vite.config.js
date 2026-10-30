import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// El proxy manda las peticiones /api/... del frontend (puerto 5173) al backend FastAPI (8000),
// así el código React puede llamar a fetch('/api/pasajeros') sin escribir el puerto.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: { '/api': 'http://127.0.0.1:8000' },
  },
})
