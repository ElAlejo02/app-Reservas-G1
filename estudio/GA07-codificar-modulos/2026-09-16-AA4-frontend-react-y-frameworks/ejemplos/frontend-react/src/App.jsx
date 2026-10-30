// Componente principal: arma la página con los otros componentes y habla con la API.
// Enseña: useEffect (cargar datos al abrir) y cómo un padre pasa datos y funciones a sus hijos.
import { useEffect, useState } from 'react'
import ContadorReservas from './componentes/ContadorReservas.jsx'
import FormularioPasajero from './componentes/FormularioPasajero.jsx'
import TablaPasajeros from './componentes/TablaPasajeros.jsx'

export default function App() {
  const [pasajeros, setPasajeros] = useState([])
  const [estado, setEstado] = useState('Conectando con el servidor…')

  async function cargarPasajeros() {
    const respuesta = await fetch('/api/pasajeros') // GET al backend FastAPI
    setPasajeros(await respuesta.json())
  }

  async function eliminar(documento) {
    await fetch(`/api/pasajeros/${documento}`, { method: 'DELETE' })
    cargarPasajeros()
  }

  // useEffect con [] se ejecuta una sola vez, cuando la página abre.
  useEffect(() => {
    fetch('/api/estado')
      .then((r) => r.json())
      .then((d) => setEstado(d.mensaje))
      .catch(() => setEstado('Sin conexión con el servidor (¿está corriendo uvicorn?)'))
    cargarPasajeros()
  }, [])

  return (
    <main>
      <header>
        <h1>Reservas HyD · Pasajeros</h1>
        <p className="estado">{estado}</p>
      </header>
      <FormularioPasajero onGuardado={cargarPasajeros} />
      <ContadorReservas tarifa={250000} />
      <TablaPasajeros pasajeros={pasajeros} onEliminar={eliminar} />
    </main>
  )
}
