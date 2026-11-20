import { useState, useEffect } from "react";
import MensajeAlerta from "./mensajealerta";

/**
 * Columna izquierda del panel operativo.
 * Carga catálogos desde MySQL, consulta disponibilidad hotelera y solicita la liquidación.
 */
export default function FormularioCotizacion({ apiUrl, onCalcularExito }) {
  const [destinos, setDestinos] = useState([]);
  const [actividades, setActividades] = useState([]);
  const [tarifasDisponibles, setTarifasDisponibles] = useState([]);

  const [destino, setDestino] = useState("");
  const [fechaEntrada, setFechaEntrada] = useState("");
  const [fechaSalida, setFechaSalida] = useState("");
  const [adultos, setAdultos] = useState(2);
  const [ninos, setNinos] = useState(0);
  const [idTarifa, setIdTarifa] = useState("");
  const [actividadesElegidas, setActividadesElegidas] = useState([]);
  const [descuentoPorcentaje, setDescuentoPorcentaje] = useState(0);
  const [clienteNombre, setClienteNombre] = useState("");
  const [clienteCorreo, setClienteCorreo] = useState("");

  const [alerta, setAlerta] = useState({ tipo: "", mensaje: "" });

  useEffect(() => {
    fetch(`${apiUrl}/destinos`)
      .then((res) => res.json())
      .then((data) => setDestinos(data))
      .catch(() =>
        setAlerta({ tipo: "error", mensaje: "No se pudieron cargar los destinos desde FastAPI." })
      );
  }, [apiUrl]);

  const manejarCambioDestino = async (codigo) => {
    setDestino(codigo);
    setTarifasDisponibles([]);
    setIdTarifa("");
    setActividadesElegidas([]);

    if (!codigo) {
      setActividades([]);
      return;
    }

    try {
      const res = await fetch(`${apiUrl}/actividades?destino=${codigo}`);
      const data = await res.json();
      setActividades(data);
    } catch {
      setActividades([]);
    }
  };

  const alternarActividad = (idAct) => {
    setActividadesElegidas((prev) =>
      prev.includes(idAct) ? prev.filter((id) => id !== idAct) : [...prev, idAct]
    );
  };

  const consultarDisponibilidad = async () => {
    setAlerta({ tipo: "", mensaje: "" });
    if (!destino || !fechaEntrada || !fechaSalida) {
      setAlerta({ tipo: "error", mensaje: "Selecciona destino, fecha de entrada y fecha de salida." });
      return;
    }

    try {
      const res = await fetch(`${apiUrl}/disponibilidad`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          destino,
          fecha_entrada: fechaEntrada,
          fecha_salida: fechaSalida,
          adultos: Number(adultos),
          ninos: Number(ninos),
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        const msg = Array.isArray(data.detail) ? data.detail[0]?.msg : data.detail;
        setAlerta({ tipo: "error", mensaje: msg || "Error consultando disponibilidad." });
        return;
      }

      setTarifasDisponibles(data);
      if (data.length === 0) {
        setAlerta({ tipo: "error", mensaje: "No hay hoteles disponibles para esas fechas/personas." });
      }
    } catch {
      setAlerta({ tipo: "error", mensaje: "Error de conexión con el servidor." });
    }
  };

  const calcularCotizacion = async (e) => {
    e.preventDefault();
    setAlerta({ tipo: "", mensaje: "" });

    if (!idTarifa) {
      setAlerta({ tipo: "error", mensaje: "Primero consulta y elige un hotel disponible." });
      return;
    }

    const solicitud = {
      destino,
      fecha_entrada: fechaEntrada,
      fecha_salida: fechaSalida,
      adultos: Number(adultos),
      ninos: Number(ninos),
      id_tarifa: Number(idTarifa),
      actividades: actividadesElegidas.map((id) => ({
        id_actividad: id,
        adultos: Number(adultos),
        ninos: Number(ninos),
      })),
      descuento_porcentaje: Number(descuentoPorcentaje) || 0,
    };

    try {
      const res = await fetch(`${apiUrl}/cotizaciones/calcular`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(solicitud),
      });

      const desglose = await res.json();
      if (!res.ok) {
        const msg = Array.isArray(desglose.detail) ? desglose.detail[0]?.msg : desglose.detail;
        setAlerta({ tipo: "error", mensaje: msg || "No se pudo calcular la liquidación." });
        return;
      }

      onCalcularExito(desglose, {
        ...solicitud,
        cliente_nombre: clienteNombre,
        cliente_correo: clienteCorreo,
      });
    } catch {
      setAlerta({ tipo: "error", mensaje: "Error de conexión al calcular." });
    }
  };

  return (
    <section className="panel-card">
      <h2>Nueva Cotización / Reserva Mayorista</h2>
      <MensajeAlerta tipo={alerta.tipo} mensaje={alerta.mensaje} />

      <form onSubmit={calcularCotizacion}>
        <div className="fila-dos">
          <div className="campo">
            <label>Destino*</label>
            <select value={destino} onChange={(e) => manejarCambioDestino(e.target.value)} required>
              <option value="">Seleccione destino...</option>
              {destinos.map((d) => (
                <option key={d.codigo} value={d.codigo}>
                  {d.nombre} ({d.codigo})
                </option>
              ))}
            </select>
          </div>

          <div className="campo">
            <label>Descuento autorizado (%)</label>
            <input
              type="number"
              min="0"
              max="15"
              value={descuentoPorcentaje}
              onChange={(e) => setDescuentoPorcentaje(e.target.value)}
            />
          </div>
        </div>

        <div className="fila-dos">
          <div className="campo">
            <label>Fecha de Entrada (Check-In)*</label>
            <input
              type="date"
              value={fechaEntrada}
              onChange={(e) => setFechaEntrada(e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label>Fecha de Salida (Check-Out)*</label>
            <input
              type="date"
              value={fechaSalida}
              onChange={(e) => setFechaSalida(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="fila-dos">
          <div className="campo">
            <label>Adultos*</label>
            <input
              type="number"
              min="1"
              max="10"
              value={adultos}
              onChange={(e) => setAdultos(e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label>Niños</label>
            <input
              type="number"
              min="0"
              max="10"
              value={ninos}
              onChange={(e) => setNinos(e.target.value)}
            />
          </div>
        </div>

        <button type="button" onClick={consultarDisponibilidad} className="btn-secundario">
          1. Consultar Hoteles y Tarifas Disponibles
        </button>

        <div className="campo" style={{ marginTop: "15px" }}>
          <label>Acomodación / Hotel Disponible*</label>
          <select value={idTarifa} onChange={(e) => setIdTarifa(e.target.value)} required>
            <option value="">Seleccione opción...</option>
            {tarifasDisponibles.map((op) => (
              <option key={op.id_tarifa} value={op.id_tarifa}>
                {op.hotel} ({op.estrellas}★) - {op.tipo_habitacion} [{op.temporada}] — $
                {op.precio_estadia.toLocaleString("es-CO")} COP
              </option>
            ))}
          </select>
        </div>

        {actividades.length > 0 && (
          <div className="campo">
            <label>Actividades y Tours Adicionales</label>
            <div className="caja-actividades">
              {actividades.map((act) => (
                <label key={act.id_actividad} className="item-actividad">
                  <input
                    type="checkbox"
                    checked={actividadesElegidas.includes(act.id_actividad)}
                    onChange={() => alternarActividad(act.id_actividad)}
                  />
                  <span>
                    <strong>{act.nombre}</strong> — Adulto: ${act.precio_adulto.toLocaleString("es-CO")}
                  </span>
                </label>
              ))}
            </div>
          </div>
        )}

        <div className="separador-cliente">
          <h3>Datos del Cliente / Agencia</h3>
          <div className="fila-dos">
            <div className="campo">
              <label>Nombre del Cliente*</label>
              <input
                type="text"
                value={clienteNombre}
                onChange={(e) => setClienteNombre(e.target.value)}
                placeholder="Ej. Agencia Viajes del Sol"
                required
              />
            </div>
            <div className="campo">
              <label>Correo del Cliente*</label>
              <input
                type="email"
                value={clienteCorreo}
                onChange={(e) => setClienteCorreo(e.target.value)}
                placeholder="cliente@correo.com"
                required
              />
            </div>
          </div>
        </div>

        <button type="submit" className="btn-verde">
          2. Calcular y Procesar Cotización
        </button>
      </form>
    </section>
  );
}
