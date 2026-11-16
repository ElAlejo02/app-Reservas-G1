// =========================================================================
// 1. CATÁLOGO DE OPCIONES (Lo que el sistema responde según la búsqueda)
// =========================================================================
const tiposAlojamiento = [
    { nombre: "Habitación 1 cama con baño privado", capacidadMax: 2, precioNoche: 140000, descripcion: "Ideal para 1 o 2 personas. Incluye Wi-Fi y aire acondicionado." },
    { nombre: "Habitación con 2 camas y baño privado", capacidadMax: 3, precioNoche: 190000, descripcion: "Comodidad total para amigos o familias pequeñas hasta 3 personas." },
    { nombre: "Habitación de dos camarotes y baño compartido", capacidadMax: 4, precioNoche: 110000, descripcion: "Opción económica grupal (máximo 4 personas)." },
    { nombre: "Apataestudio equipado", capacidadMax: 2, precioNoche: 175000, descripcion: "Espacio independiente con cocineta y baño privado." },
    { nombre: "Apartamento completo", capacidadMax: 6, precioNoche: 320000, descripcion: "Sala, cocina integral, 2 alcobas y hasta 6 huéspedes." },
    { nombre: "Cabaña campestre / ecológica", capacidadMax: 10, precioNoche: 450000, descripcion: "Rodeada de naturaleza, terraza privada y capacidad para grupos grandes." }
];

const rutasTransporte = [
    { tipo: "vuelos", aerolinea: "Aerolínea Nacional", precioPorPersona: 350000, detalle: "Vuelo directo con equipaje de mano incluido." },
    { tipo: "autobus", aerolinea: "Expreso Intermunicipal", precioPorPersona: 65000, detalle: "Bus climatizado de lujo con sillas reclinables." }
];

let categoriaActual = "vuelos";

// =========================================================================
// 2. REFERENCIAS AL HTML
// =========================================================================
const botonesTabs = document.querySelectorAll(".tab-btn");
const titulo = document.getElementById("titulo-categoria");
const subtitulo = document.getElementById("subtitulo-categoria");
const opcionesTrayecto = document.getElementById("opciones-trayecto");
const selectorPaquete = document.getElementById("selector-transporte-paquete");
const campoOrigen = document.getElementById("campo-origen");
const inputOrigen = document.getElementById("input-origen");
const labelIda = document.getElementById("label-ida");
const labelVuelta = document.getElementById("label-vuelta");
const labelPersonas = document.getElementById("label-personas");
const inputPersonas = document.getElementById("input-personas");
const btnBuscar = document.getElementById("btn-buscar-texto");
const formulario = document.getElementById("form-busqueda");
const contenedorResultados = document.getElementById("contenedor-resultados");

// =========================================================================
// 3. CAMBIO ENTRE LAS 4 PESTAÑAS
// =========================================================================
botonesTabs.forEach(boton => {
    boton.addEventListener("click", () => {
        botonesTabs.forEach(b => b.classList.remove("active"));
        boton.classList.add("active");
        categoriaActual = boton.getAttribute("data-tab");
        contenedorResultados.innerHTML = "";

        if (categoriaActual === "vuelos" || categoriaActual === "autobus") {
            titulo.textContent = categoriaActual === "vuelos" ? "Reserva tu vuelo al mejor precio" : "Viaja en autobús por toda Colombia";
            subtitulo.textContent = "Recuerda que pueden elegir hasta 12 personas por reserva.";
            opcionesTrayecto.style.display = "flex";
            selectorPaquete.style.display = "none";
            campoOrigen.style.display = "flex";
            inputOrigen.required = true;
            labelIda.textContent = "Fecha de ida*";
            labelVuelta.textContent = "Fecha de vuelta*";
            labelPersonas.textContent = "Pasajeros (máx. 12)*";
            inputPersonas.max = "12";
            btnBuscar.textContent = categoriaActual === "vuelos" ? "Buscar vuelos" : "Buscar autobús";
        } 
        else if (categoriaActual === "alojamientos") {
            titulo.textContent = "Encuentra tu alojamiento ideal";
            subtitulo.textContent = "Selecciona tu destino, fechas y cuántas personas se hospedarán.";
            opcionesTrayecto.style.display = "none"; // Oculta ida/vuelta
            campoOrigen.style.display = "none";    // Oculta origen
            inputOrigen.required = false;
            labelIda.textContent = "Fecha de llegada*";
            labelVuelta.textContent = "Fecha de salida*";
            labelPersonas.textContent = "¿Cuántas personas?*";
            inputPersonas.removeAttribute("max");  // Permite ingresar cualquier número
            btnBuscar.textContent = "Buscar alojamientos";
        } 
        else if (categoriaActual === "paquetes") {
            titulo.textContent = "Arma tu viaje: Transporte + Alojamiento con descuento";
            subtitulo.textContent = "Combina tu medio de transporte favorito con hospedaje y ahorra en el total.";
            opcionesTrayecto.style.display = "flex";
            selectorPaquete.style.display = "block";
            campoOrigen.style.display = "flex";
            inputOrigen.required = true;
            labelIda.textContent = "Fecha de ida*";
            labelVuelta.textContent = "Fecha de regreso*";
            labelPersonas.textContent = "¿Cuántas personas viajan?*";
            inputPersonas.max = "12";
            btnBuscar.textContent = "Buscar paquetes";
        }
    });
});

// =========================================================================
// 4. PROCESAMIENTO DE DATOS AL PRESIONAR BUSCAR
// =========================================================================
formulario.addEventListener("submit", (e) => {
    e.preventDefault();

    const origen = inputOrigen.value.trim();
    const destino = document.getElementById("input-destino").value.trim();
    const fechaIda = document.getElementById("fecha-ida").value;
    const fechaVuelta = document.getElementById("fecha-vuelta").value;
    const cantidadPersonas = parseInt(inputPersonas.value);

    // Validación básica de fechas
    if (fechaVuelta && fechaVuelta < fechaIda) {
        contenedorResultados.innerHTML = `<p class="alerta-error">La fecha de salida/regreso no puede ser anterior a la fecha inicial.</p>`;
        return;
    }

    let html = "";

    // CASO A: ALOJAMIENTOS (Filtra habitaciones/cabañas según la cantidad de personas)
    if (categoriaActual === "alojamientos") {
        if (!fechaVuelta) {
            contenedorResultados.innerHTML = `<p class="alerta-error">Por favor selecciona la fecha de salida del alojamiento.</p>`;
            return;
        }

        // Filtramos solo los alojamientos donde quepan las personas ingresadas
        const opcionesValidas = tiposAlojamiento.filter(hab => hab.capacidadMax >= cantidadPersonas);

        html += `<div class="resumen-busqueda">Alojamientos disponibles en <strong>${destino}</strong> para <strong>${cantidadPersonas} persona(s)</strong> (Del ${fechaIda} al ${fechaVuelta}):</div><div class="grid-ofertas">`;

        if (opcionesValidas.length === 0) {
            html += `<p class="alerta-error">Para grupos mayores a 10 personas te recomendamos reservar dos cabañas contiguas o contactarnos directamente.</p>`;
        } else {
            opcionesValidas.forEach(hab => {
                html += `
                    <div class="tarjeta-oferta">
                        <div>
                            <h4>${hab.nombre} (Capacidad máx: ${hab.capacidadMax} personas)</h4>
                            <p>${hab.descripcion}</p>
                        </div>
                        <div class="oferta-precio">
                            <span>$${hab.precioNoche.toLocaleString('es-CO')} COP / noche</span>
                            <button type="button" onclick="irAReservar('${hab.nombre}', '${hab.precioNoche}', '${destino}', '${fechaIda}', ${cantidadPersonas})">Elegir</button>
                        </div>
                    </div>
                `;
            });
        }
        html += `</div>`;
    }

    // CASO B: VUELOS O AUTOBÚS
    else if (categoriaActual === "vuelos" || categoriaActual === "autobus") {
        const ruta = rutasTransporte.find(r => r.tipo === categoriaActual);
        const total = ruta.precioPorPersona * cantidadPersonas;

        html += `
            <div class="resumen-busqueda">Resultados de <strong>${categoriaActual.toUpperCase()}</strong> de <strong>${origen}</strong> hacia <strong>${destino}</strong> para <strong>${cantidadPersonas} pasajero(s)</strong>:</div>
            <div class="grid-ofertas">
                <div class="tarjeta-oferta">
                    <div>
                        <h4>${ruta.aerolinea}: ${origen} - ${destino}</h4>
                        <p>${ruta.detalle} | Fecha: ${fechaIda}</p>
                    </div>
                    <div class="oferta-precio">
                        <span>Total: $${total.toLocaleString('es-CO')} COP</span>
                        <button type="button" onclick="irAReservar('${categoriaActual.toUpperCase()} ${origen}-${destino}', '${total}', '${destino}', '${fechaIda}', ${cantidadPersonas})">Reservar</button>
                    </div>
                </div>
            </div>
        `;
    }

    // CASO C: ARMA TU VIAJE (Transporte + Alojamiento con descuento)
    else if (categoriaActual === "paquetes") {
        const medio = document.getElementById("medio-transporte").value;
        const descuento = medio === "Vuelo" ? 0.15 : 0.20;
        const opcionesHab = tiposAlojamiento.filter(hab => hab.capacidadMax >= cantidadPersonas);

        html += `<div class="resumen-busqueda">Paquetes <strong>${medio} + Alojamiento</strong> hacia <strong>${destino}</strong> (${cantidadPersonas} personas) con <strong>${descuento * 100}% de descuento aplicado</strong>:</div><div class="grid-ofertas">`;