import { useState, useEffect } from "react";
import MensajeAlerta from "./mensajealerta";

/**
 * Columna derecha del panel operativo.
 * Muestra el desglose financiero recibido por props y confirma la reserva en MySQL.
 */
export default function ResumenLiquidacion({ apiUrl, token, desglose, solicitud }) {
  const [guardando, setGuardando] = useState(false);
  const [confirmada, setConfirmada] = useState(false);
  const [alerta, setAlerta] = useState({ tipo: "", mensaje: "" });

  useEffect(() => {
    setConfirmada(false);
    setAlerta({ tipo: "", mensaje: "" });
  }, [desglose]);

  const confirmarYGuardar = async () => {
    if (!solicitud) return;
    setGuardando(true);
    setAlerta({ tipo: "", mensaje: "" });

    try {
      const res = await fetch(`${apiUrl}/cotizaciones`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(solicitud),
      });

      const data = await res.json();
      if (!res.ok) {
        setAlerta({ tipo: "error", mensaje: data.detail || "No se pudo guardar en MySQL." });
        setGuardando(false);
        return;
      }

      setConfirmada(true);
      setAlerta({
        tipo: "exito",
        mensaje: `¡Reserva almacenada con éxito! Código oficial: ${data.codigo} (Estado: ${data.estado})`,
      });
    } catch {
      setAlerta({ tipo: "error", mensaje: "Error de red al guardar la cotización." });
    } finally {
      setGuardando(false);
    }
  };

  return (
    <aside className="panel-card">
      <h2>Resumen de Liquidación</h2>

      {!desglose ? (
        <div className="estado-vacio">
          <p>
            Ingrese los datos de la izquierda y presione{" "}
            <strong>"Calcular y Procesar Cotización"</strong> para generar la liquidación
            automática desde el servidor.
          </p>
        </div>
      ) : (
        <div>
          <div className="resumen-cabecera">
            <strong>{desglose.hotel}</strong> — Destino: {desglose.destino}
            <br />
            Acomodación: {desglose.tipo_habitacion} (Temporada {desglose.temporada})
          </div>

          <ul className="lista-valores">
            <li>
              <span>Total de Noches</span>
              <strong>{desglose.noches}</strong>
            </li>
            <li>
              <span>Valor Estadía Hotel</span>
              <strong>${desglose.precio_hotel.toLocaleString("es-CO")}</strong>
            </li>
            <li>
              <span>Adicional Actividades</span>
              <strong>${desglose.precio_actividades.toLocaleString("es-CO")}</strong>
            </li>
            <li>
              <span>Subtotal</span>
              <strong>${desglose.subtotal.toLocaleString("es-CO")}</strong>
            </li>
            <li>
              <span>Descuento ({desglose.descuento_porcentaje}%)</span>
              <strong>-${desglose.descuento.toLocaleString("es-CO")}</strong>
            </li>
            <li>
              <span>IVA ({desglose.iva_porcentaje}%)</span>
              <strong>${desglose.iva.toLocaleString("es-CO")}</strong>
            </li>
            <li>
              <span>Tasas del destino</span>
              <strong>${desglose.tasas.toLocaleString("es-CO")}</strong>
            </li>
          </ul>

          <div className="total-destacado">
            <span>VALOR TOTAL:</span>
            <strong>${desglose.total.toLocaleString("es-CO")} COP</strong>
          </div>

          <button
            type="button"
            onClick={confirmarYGuardar}
            className="btn-dorado"
            disabled={guardando || confirmada}
          >
            {confirmada
              ? "Reserva Confirmada"
              : guardando
              ? "Guardando en MySQL..."
              : "Confirmar y Guardar Reserva"}
          </button>

          <MensajeAlerta tipo={alerta.tipo} mensaje={alerta.mensaje} />
        </div>
      )}
    </aside>
  );
}
