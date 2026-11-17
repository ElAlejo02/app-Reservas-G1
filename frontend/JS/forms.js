// Referencias a los dos formularios y botones de cambio
const formLogin = document.getElementById("form-login");
const formRegistro = document.getElementById("form-registro");
const btnIrRegistro = document.getElementById("btn-ir-registro");
const btnIrLogin = document.getElementById("btn-ir-login");
const mensajeEstado = document.getElementById("mensaje-estado");
const cajaReserva = document.getElementById("resumen-reserva-pendiente");

// 1. Verificar si existe una reserva guardada desde Vuelos.html
const reservaGuardada = localStorage.getItem("reservaPendiente");
if (reservaGuardada) {
    const datos = JSON.parse(reservaGuardada);
    cajaReserva.style.display = "block";
    cajaReserva.innerHTML = `
        <strong>Reserva seleccionada:</strong> ${datos.servicio}<br>
        Destino: ${datos.destino} | Fecha: ${datos.fecha} | Personas: ${datos.personas}<br>
        Total estimado: <strong>$${Number(datos.precio).toLocaleString('es-CO')} COP</strong>
    `;
}

// 2. Alternar hacia el formulario de Crear Cuenta
btnIrRegistro.addEventListener("click", () => {
    formLogin.style.display = "none";
    formRegistro.style.display = "block";
    mensajeEstado.style.display = "none";
});

// 3. Alternar hacia el formulario de Iniciar Sesión
btnIrLogin.addEventListener("click", () => {
    formRegistro.style.display = "none";
    formLogin.style.display = "block";
    mensajeEstado.style.display = "none";
});

// 4. Procesar envío de Inicio de Sesión
formLogin.addEventListener("submit", (e) => {
    e.preventDefault();
    const usuario = document.getElementById("login-usuario").value.trim();

    mensajeEstado.style.display = "block";
    mensajeEstado.innerHTML = `Bienvenido de nuevo, <strong>${usuario}</strong>. Tu sesión se ha iniciado correctamente.`;
    
    // Limpiar reserva pendiente si existía
    localStorage.removeItem("reservaPendiente");
});

// 5. Procesar envío de Registro Nuevo
formRegistro.addEventListener("submit", (e) => {
    e.preventDefault();
    const nombre = document.getElementById("reg-nombre").value.trim();
    const correo = document.getElementById("reg-correo").value.trim();

    // Guardar perfil básico en localStorage
    localStorage.setItem("usuarioRegistrado", JSON.stringify({ nombre, correo }));

    mensajeEstado.style.display = "block";
    mensajeEstado.innerHTML = `Cuenta creada con éxito para <strong>${nombre}</strong>. Hemos enviado los detalles a <strong>${correo}</strong>.`;
    
    localStorage.removeItem("reservaPendiente");
});// 4. Procesar envío de Inicio de Sesión
formLogin.addEventListener("submit", (e) => {
    e.preventDefault();
    const usuario = document.getElementById("login-usuario").value.trim();

    // Guardamos la sesión activa para que cotizador.html deje entrar al asesor
    localStorage.setItem("token", "sesion-activa");
    localStorage.setItem("usuarioActivo", JSON.stringify({ nombre: usuario, rol: "ASESOR" }));

    mensajeEstado.style.display = "block";
    mensajeEstado.innerHTML = `Bienvenido de nuevo, <strong>${usuario}</strong>. Ingresando al módulo de cotizaciones...`;
    
    localStorage.removeItem("reservaPendiente");

    // Redirige a la página de cotizaciones después de 1 segundo
    setTimeout(() => {
        window.location.href = "cotizador.html";
    }, 1000);
});
