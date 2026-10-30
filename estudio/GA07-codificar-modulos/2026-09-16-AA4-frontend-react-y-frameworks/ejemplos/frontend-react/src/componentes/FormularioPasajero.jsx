// Componente funcional: formulario para registrar un pasajero.
// Enseña: estado con useState, eventos onChange y onSubmit, y props (onGuardado).
import { useState } from 'react'

const VACIO = { documento: '', nombre: '', edad: '', genero: '' }

export default function FormularioPasajero({ onGuardado }) {
  // Estado del formulario: cada campo vive aquí, no en el HTML.
  const [datos, setDatos] = useState(VACIO)
  const [mensaje, setMensaje] = useState({ texto: '', error: false })

  // Evento onChange: se dispara con cada tecla y actualiza solo el campo que cambió.
  function cambiar(evento) {
    const { name, value } = evento.target
    setDatos({ ...datos, [name]: value })
  }

  // Evento onSubmit: envía los datos a la API (POST) sin recargar la página.
  async function guardar(evento) {
    evento.preventDefault()
    const respuesta = await fetch('/api/pasajeros', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...datos, edad: Number(datos.edad) }),
    })
    if (respuesta.ok) {
      setMensaje({ texto: 'Pasajero guardado', error: false })
      setDatos(VACIO)
      onGuardado() // avisa al componente padre (App) para que recargue la tabla
    } else {
      const cuerpo = await respuesta.json()
      const detalle = typeof cuerpo.detail === 'string' ? cuerpo.detail : 'Revisa los datos'
      setMensaje({ texto: detalle, error: true })
    }
  }

  return (
    <form className="tarjeta" onSubmit={guardar}>
      <h2>Registrar pasajero</h2>
      <div className="fila">
        <label>
          Documento
          <input name="documento" value={datos.documento} onChange={cambiar} required />
        </label>
        <label className="ancho">
          Nombre completo
          <input name="nombre" value={datos.nombre} onChange={cambiar} required />
        </label>
      </div>
      <div className="fila">
        <label>
          Edad
          <input name="edad" type="number" min="0" max="120" value={datos.edad} onChange={cambiar} required />
        </label>
        <label>
          Género
          <select name="genero" value={datos.genero} onChange={cambiar} required>
            <option value="">Seleccione…</option>
            <option>Masculino</option>
            <option>Femenino</option>
            <option>Otro</option>
          </select>
        </label>
      </div>
      <button type="submit">Guardar</button>
      {mensaje.texto && <p className={mensaje.error ? 'error' : 'ok'}>{mensaje.texto}</p>}
    </form>
  )
}
