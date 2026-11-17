// Sugerencias de destinos reales desde el Backend (si está encendido)
fetch("http://127.0.0")
    .then(res => res.json())
    .then(destinos => {
        const datalist = document.getElementById("lista-destinos-api");
        if (datalist) {
            destinos.forEach(d => {
                datalist.innerHTML += `<option value="${d.nombre} (${d.codigo})"></option>`;
            });
        }
    })
    .catch(() => {});

let categoriaActual = "vuelos";

const botonesTabs = document.querySelectorAll(".tab-btn");
const titulo = document.getElementById("titulo-categoria");
const subtitulo = document.getElementById("subtitulo-categoria");
const opcionesTrayecto = document.getElementById("opciones-trayecto");
const campoOrigen = document.getElementById("campo-origen");
const inputOrigen = document.getElementById("input-origen");
const labelIda = document.getElementById("label-ida");
const labelVuelta = document.getElementById("label-vuelta");
const labelPersonas = document.getElementById("label-personas");
const inputPersonas = document.getElementById("input-personas");
const btnBuscar = document.getElementById("btn-buscar-texto");
const formulario = document.getElementById("form-busqueda");
const contenedorResultados = document.getElementById("contenedor-resultados");

// Cambio de pestañas (Vuelos, Alojamientos, Arma tu viaje)
botonesTabs.forEach(boton => {
    boton.addEventListener("click", () => {
        botonesTabs.forEach(b => b.classList.remove("active"));
        boton.classList.add("active");
        categoriaActual = boton.getAttribute("data-tab");
        contenedorResultados.innerHTML = "";

        if (categoriaActual === "vuelos") {
            titulo.textContent = "Reserva tu vuelo al mejor precio";
            subtitulo.textContent = "Recuerda que pueden elegir hasta 12 personas por reserva.";
            opcionesTrayecto.style.display = "flex";
            campoOrigen.style.display = "flex";
            inputOrigen.required = true;
            labelIda.textContent = "Fecha de ida*";
            labelVuelta.textContent = "Fecha de vuelta*";
            labelPersonas.textContent = "Pasajeros (máx. 12)*";
            inputPersonas.max = "12";
            btnBuscar.textContent = "Cotizar vuelos";
        } 
        else if (categoriaActual === "alojamientos") {
            titulo.textContent = "Encuentra tu alojamiento ideal";
            subtitulo.textContent = "Selecciona tu destino, fechas y cuántas personas se hospedarán.";
            opcionesTrayecto.style.display = "none";
            campoOrigen.style.display = "none";
            inputOrigen.required = false;
            labelIda.textContent = "Fecha de llegada*";
            labelVuelta.textContent = "Fecha de salida*";
            labelPersonas.textContent = "¿Cuántas personas?*";
            inputPersonas.removeAttribute("max");
            btnBuscar.textContent = "Cotizar alojamiento";
        } 
        else if (categoriaActual === "paquetes") {
            titulo.textContent = "Arma tu viaje: Vuelo + Alojamiento con descuento";
            subtitulo.textContent = "Combina tu vuelo con hospedaje y ahorra en el total.";
            opcionesTrayecto.style.display = "flex";
            campoOrigen.style.display = "flex";
            inputOrigen.required = true;
            labelIda.textContent = "Fecha de ida*";
            labelVuelta.textContent = "Fecha de regreso*";
            labelPersonas.textContent = "¿Cuántas personas viajan?*";
            inputPersonas.max = "12";
            btnBuscar.textContent = "Armar paquete";
        }
    });
});

// Al darle clic al botón de abajo ("Cotizar vuelos", "Cotizar alojamiento" o "Armar paquete")
formulario.addEventListener("submit", (e) => {
    e.preventDefault();

    const origen = inputOrigen.value.trim();
    const destino = document.getElementById("input-destino").value.trim();
    const fechaIda = document.getElementById("fecha-ida").value;
    const fechaVuelta = document.getElementById("fecha-vuelta").value;
    const cantidadPersonas = parseInt(inputPersonas.value);

    if (fechaVuelta && fechaVuelta < fechaIda) {
        contenedorResultados.innerHTML = `<p class="alerta-error">La fecha de salida/regreso no puede ser anterior a la fecha inicial.</p>`;
        return;
    }

    const nombresServicio = {
        vuelos: `Vuelo ${origen} - ${destino}`,
        alojamientos: `Alojamiento en ${destino}`,
        paquetes: `Paquete Vuelo + Alojamiento (${origen} - ${destino})`
    };

    // Guarda los datos ingresados y lleva directo al registro / acceso (forms.html)
    const datosParaCotizar = {
        servicio: nombresServicio[categoriaActual],
        destino: destino,
        fecha: fechaIda,
        personas: cantidadPersonas
    };

    localStorage.setItem("reservaPendiente", JSON.stringify(datosParaCotizar));
    window.location.href = "forms.html";
});
