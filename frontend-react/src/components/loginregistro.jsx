import { useState } from "react";
import MensajeAlerta from "./mensajealerta";

/**
 * Componente de autenticación (Iniciar Sesión) y Registro de Asesores.
 * Se conecta mediante fetch() con los endpoints /auth/login y /auth/registro de FastAPI.
 */
export default function LoginRegistro({ apiUrl, onLoginExitoso }) {
  const [esRegistro, setEsRegistro] = useState(false);
  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [clave, setClave] = useState("");
  const [alerta, setAlerta] = useState({ tipo: "", mensaje: "" });
  const [cargando, setCargando] = useState(false);

  const manejarEnvio = async (e) => {
    e.preventDefault();
    setAlerta({ tipo: "", mensaje: "" });
    setCargando(true);

    const ruta = esRegistro ? "/auth/registro" : "/auth/login";
    const cuerpo = esRegistro ? { nombre, correo, clave } : { correo, clave };

    try {
      const respuesta = await fetch(`${apiUrl}${ruta}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cuerpo),
      });

      const data = await respuesta.json();

      if (!respuesta.ok) {
        const detalle = Array.isArray(data.detail) ? data.detail[0]?.msg : data.detail;
        setAlerta({
          tipo: "error",
          mensaje: detalle || "Credenciales inválidas o datos incompletos.",
        });
        setCargando(false);
        return;
      }

      if (esRegistro) {
        setAlerta({
          tipo: "exito",
          mensaje: `Cuenta creada para ${data.nombre}. Ahora inicia sesión.`,
        });
        setEsRegistro(false);
        setClave("");
      } else {
        onLoginExitoso(data.access_token, data.usuario);
      }
    } catch {
      setAlerta({
        tipo: "error",
        mensaje: "No se pudo conectar con el servidor Backend (puerto 8000).",
      });
    } finally {
      setCargando(false);
    }
  };

  return (
    <main className="auth-container">
      <section className="auth-card">
        <div className="auth-header">
          <h2>{esRegistro ? "Crear Cuenta de Asesor" : "Ingreso al Sistema"}</h2>
          <p>Hoteles y Destinos — Gestión Mayorista</p>
        </div>

        <MensajeAlerta tipo={alerta.tipo} mensaje={alerta.mensaje} />

        <form onSubmit={manejarEnvio}>
          {esRegistro && (
            <div className="campo">
              <label>Nombre completo*</label>
              <input
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                placeholder="Ej. Laura Vergara"
                required
              />
            </div>
          )}

          <div className="campo">
            <label>Correo electrónico*</label>
            <input
              type="email"
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              placeholder="asesor@hotelesydestinos.com"
              required
            />
          </div>

          <div className="campo">
            <label>Contraseña*</label>
            <input
              type="password"
              value={clave}
              onChange={(e) => setClave(e.target.value)}
              placeholder="Mínimo 8 caracteres (letras y números)"
              required
            />
          </div>

          <button type="submit" className="btn-dorado" disabled={cargando}>
            {cargando ? "Procesando..." : esRegistro ? "Registrarme" : "Ingresar al Sistema"}
          </button>
        </form>

        <div className="auth-switch">
          <button
            type="button"
            className="btn-link"
            onClick={() => {
              setEsRegistro(!esRegistro);
              setAlerta({ tipo: "", mensaje: "" });
            }}
          >
            {esRegistro ? "¿Ya tienes cuenta? Inicia sesión" : "¿Eres asesor nuevo? Regístrate aquí"}
          </button>
        </div>
      </section>
    </main>
  );
}
