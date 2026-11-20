/**
 * Componente reutilizable para mostrar notificaciones visuales (Feedback UX).
 * @param {string} tipo - Define el estilo visual: 'exito' o 'error'.
 * @param {string} mensaje - Texto informativo que se muestra al usuario.
 */
export default function MensajeAlerta({ tipo, mensaje }) {
  if (!mensaje) return null;

  return (
    <div className={`alerta alerta-${tipo}`} role="alert">
      {mensaje}
    </div>
  );
}
