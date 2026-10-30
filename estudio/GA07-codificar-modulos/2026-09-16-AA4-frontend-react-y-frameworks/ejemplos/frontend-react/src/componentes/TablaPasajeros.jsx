// Componente funcional que solo muestra datos: recibe la lista por props y la pinta.
// Enseña: props, listas con map() y la propiedad key.
export default function TablaPasajeros({ pasajeros, onEliminar }) {
  if (pasajeros.length === 0) {
    return <p className="tarjeta">No hay pasajeros registrados.</p>
  }
  return (
    <table className="tarjeta">
      <thead>
        <tr>
          <th>Documento</th>
          <th>Nombre</th>
          <th>Edad</th>
          <th>Género</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {pasajeros.map((p) => (
          // key ayuda a React a saber qué fila cambió sin redibujar todas.
          <tr key={p.documento}>
            <td>{p.documento}</td>
            <td>{p.nombre}</td>
            <td>{p.edad}</td>
            <td>{p.genero}</td>
            <td>
              {/* Evento onClick: elimina este pasajero */}
              <button className="secundario" onClick={() => onEliminar(p.documento)}>
                Eliminar
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
