const API_URL = "http://127.0.0.1:8000";

// =========================================================================
// 1. SEGURIDAD Y SESIÓN DEL ASESOR
// =========================================================================
const token = localStorage.getItem("token");
const usuarioActivo = JSON.parse(localStorage.getItem("usuarioActivo") || "null");

// Si nadie ha iniciado sesión, lo devolvemos a forms.html
if (!token || !usuarioActivo) {
    window.location.href = "forms.html";
} else {
    document.getElementById("info-asesor").textContent = `Asesor: ${usuarioActivo.nombre} (${usuarioActivo.rol})`;
}

// Botón para cerrar sesión
document.getElementById("btn-cerrar-sesion").addEventListener("click", () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuarioActivo");
    window.location.href = "forms.html";
});


// =========================================================================
// 2. REFERENCIAS A LOS ELEMENTOS DE LA PANTALLA (DOM)
// =========================================================================
const selectDestino = document.getElementById("destino");
const selectTarifa = document.getElementById("tarifa-hotel");
const cajaActividades = document.getElementById("lista-actividades");
const btnBuscarHoteles = document.getElementById("btn-buscar-hoteles");
const formCotizacion = document.getElementById("form-cotizacion");
const btnConfirmarGuardar = document.getElementById("btn-confirmar-guardar");
const bannerConfirmacion = document.getElementById("banner-confirmacion");

// Variable donde guardaremos los datos calculados antes de confirmarlos en MySQL
let solicitudListaParaGuardar = null;


// =========================================================================
// 3. CARGAR CATÁLOGO DE DESTINOS AL ABRIR LA PÁGINA (GET /destinos)
// =========================================================================
async function cargarDestinos() {
    try {
        const respuesta = await fetch(`${API_URL}/destinos`);
        if (!respuesta.ok) throw new Error("Error al consultar destinos");

        const destinos = await respuesta.json();
        selectDestino.innerHTML = `<option value="">Seleccione un destino...</option>`;

        destinos.forEach(dest => {
            selectDestino.innerHTML += `<option value="${dest.codigo}">${dest.nombre} (${dest.codigo})</option>`;
        });
    } catch (error) {
        selectDestino.innerHTML = `<option value="">No se pudo conectar con la API (puerto 8000)</option>`;
    }
}
cargarDestinos();


// =========================================================================
// 4. CARGAR ACTIVIDADES SEGÚN EL DESTINO ELEGIDO (GET /actividades)
// =========================================================================
selectDestino.addEventListener("change", async () => {
    const codigoDestino = selectDestino.value;
    selectTarifa.innerHTML = `<option value="">Presiona "Consultar Hoteles y Tarifas Disponibles"...</option>`;

    if (!codigoDestino) {
        cajaActividades.innerHTML = `<small>Selecciona un destino para ver sus actividades disponibles.</small>`;
        return;
    }

    try {
        const respuesta = await fetch(`${API_URL}/actividades?destino=${codigoDestino}`);
        const actividades = await respuesta.json();

        if (actividades.length === 0) {
            cajaActividades.innerHTML = `<small>No hay actividades registradas para este destino.</small>`;
            return;
        }

        cajaActividades.innerHTML = "";
        actividades.forEach(act => {
            cajaActividades.innerHTML += `
                <label class="item-actividad">
                    <input type="checkbox" class="chk-actividad" value="${act.id_actividad}">
                    <span>
                        <strong>${act.nombre}</strong> — Adulto: $${act.precio_adulto.toLocaleString("es-CO")} | Niño: $${act.precio_nino.toLocaleString("es-CO")}
                    </span>
                </label>
            `;
        });
    } catch (error) {
        cajaActividades.innerHTML = `<small>Error cargando actividades del destino.</small>`;
    }
});


// =========================================================================
// 5. CONSULTAR HOTELES Y TARIFAS DISPONIBLES (POST /disponibilidad)
// =========================================================================
btnBuscarHoteles.addEventListener("click", async () => {
    const datosBusqueda = {
        destino: selectDestino.value,
        fecha_entrada: document.getElementById("fecha-entrada").value,
        fecha_salida: document.getElementById("fecha-salida").value,
        adultos: parseInt(document.getElementById("adultos").value) || 0,
        ninos: parseInt(document.getElementById("ninos").value) || 0
    };

    if (!datosBusqueda.destino || !datosBusqueda.fecha_entrada || !datosBusqueda.fecha_salida) {
        alert("Por favor selecciona el destino, la fecha de entrada y la fecha de salida.");
        return;
    }

    try {
        btnBuscarHoteles.textContent = "Consultando disponibilidad...";
        const respuesta = await fetch(`${API_URL}/disponibilidad`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datosBusqueda)
        });

        const resultado = await respuesta.json();
        btnBuscarHoteles.textContent = "1. Consultar Hoteles y Tarifas Disponibles";

        if (!respuesta.ok) {
            const mensajeError = Array.isArray(resultado.detail) ? resultado.detail[0].msg : resultado.detail;
            alert(mensajeError || "Revisa las fechas o la cantidad de personas.");
            return;
        }

        if (resultado.length === 0) {
            selectTarifa.innerHTML = `<option value="">No hay habitaciones disponibles para esas fechas/personas</option>`;
            return;
        }

        selectTarifa.innerHTML = `<option value="">Seleccione hotel y tipo de acomodación...</option>`;
        resultado.forEach(opcion => {
            selectTarifa.innerHTML += `
                <option value="${opcion.id_tarifa}">
                    ${opcion.hotel} (${opcion.estrellas} estrellas) - ${opcion.tipo_habitacion} [Temporada ${opcion.temporada}] — $${opcion.precio_estadia.toLocaleString("es-CO")} COP
                </option>
            `;
        });
    } catch (error) {
        btnBuscarHoteles.textContent = "1. Consultar Hoteles y Tarifas Disponibles";
        alert("Error de conexión con el servidor Python.");
    }
});


// =========================================================================
// 6. CALCULAR LIQUIDACIÓN FINANCIERA (POST /cotizaciones/calcular)
// =========================================================================
formCotizacion.addEventListener("submit", async (e) => {
    e.preventDefault();

    const adultos = parseInt(document.getElementById("adultos").value) || 0;
    const ninos = parseInt(document.getElementById("ninos").value) || 0;
    const idTarifa = parseInt(selectTarifa.value);

    if (!idTarifa) {
        alert("Debes consultar y seleccionar una acomodación/hotel disponible primero.");
        return;
    }

    // Recolectamos las actividades que el asesor marcó con chulito
    const actividadesPedidas = [];
    document.querySelectorAll(".chk-actividad:checked").forEach(checkbox => {
        actividadesPedidas.push({
            id_actividad: parseInt(checkbox.value),
            adultos: adultos,
            ninos: ninos
        });
    });

    const solicitudCalculo = {
        destino: selectDestino.value,
        fecha_entrada: document.getElementById("fecha-entrada").value,
        fecha_salida: document.getElementById("fecha-salida").value,
        adultos: adultos,
        ninos: ninos,
        id_tarifa: idTarifa,
        actividades: actividadesPedidas,
        descuento_porcentaje: parseInt(document.getElementById("descuento").value) || 0
    };

    try {
        const respuesta = await fetch(`${API_URL}/cotizaciones/calcular`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(solicitudCalculo)
        });

        const desglose = await respuesta.json();

        if (!respuesta.ok) {
            const mensajeError = Array.isArray(desglose.detail) ? desglose.detail[0].msg : desglose.detail;
            alert(mensajeError || "No se pudo calcular la liquidación.");
            return;
        }

        // Preparamos el paquete completo con datos del cliente para el botón "Confirmar y Guardar"
        solicitudListaParaGuardar = {
            ...solicitudCalculo,
            cliente_nombre: document.getElementById("cliente-nombre").value.trim(),
            cliente_correo: document.getElementById("cliente-correo").value.trim()
        };

        // Cambiamos la vista de la columna derecha del estado vacío al desglose calculado
        document.getElementById("estado-neutro").style.display = "none";
        document.getElementById("detalle-liquidacion").style.display = "block";
        bannerConfirmacion.style.display = "none";

        btnConfirmarGuardar.disabled = false;
        btnConfirmarGuardar.textContent = "Confirmar y Guardar Reserva";

        document.getElementById("resumen-hotel-info").innerHTML = `
            <strong>${desglose.hotel}</strong> — Destino: ${desglose.destino}<br>
            Acomodación: ${desglose.tipo_habitacion} (Temporada ${desglose.temporada})
        `;

        document.getElementById("lista-desglose").innerHTML = `
            <li><span>Total de Noches</span><strong>${desglose.noches}</strong></li>
            <li><span>Valor Estadía Hotel</span><strong>$${desglose.precio_hotel.toLocaleString("es-CO")}</strong></li>
            <li><span>Adicional Actividades</span><strong>$${desglose.precio_actividades.toLocaleString("es-CO")}</strong></li>
