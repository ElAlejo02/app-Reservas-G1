/**
 * Barra superior corporativa del Módulo de Cotizaciones Mayorista.
 * Muestra el nombre y rol del asesor autenticado y permite cerrar sesión.
 */
export default function Navbar({ usuario, onCerrarSesion }) {
  return (
    <header className="topbar">
      <div className="topbar-marca">
        <h1>Hoteles y Destinos S.A.S.</h1>
        <span>Módulo Operativo de Cotizaciones Mayorista (React JS)</span>
      </div>

      <div className="topbar-usuario">
        <span>
          Asesor: <strong>{usuario.nombre}</strong> ({usuario.rol})
        </span>
        <button type="button" onClick={onCerrarSesion} className="btn-salir">
          Cerrar Sesión
        </button>
      </div>
    </header>
  );
}
