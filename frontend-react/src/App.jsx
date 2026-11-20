import { useState } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import LoginRegistro from "./components/loginregistro";
import FormularioCotizacion from "./components/cotizaciones";
import ResumenLiquidacion from "./components/liquidación";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token_react") || "");
  const [usuario, setUsuario] = useState(() =>
    JSON.parse(localStorage.getItem("usuario_react") || "null")
  );
  const [desgloseActual, setDesgloseActual] = useState(null);
  const [solicitudActual, setSolicitudActual] = useState(null);

  const manejarLoginExitoso = (nuevoToken, datosUsuario) => {
    localStorage.setItem("token_react", nuevoToken);
    localStorage.setItem("usuario_react", JSON.stringify(datosUsuario));
    setToken(nuevoToken);
    setUsuario(datosUsuario);
  };

  const manejarCerrarSesion = () => {
    localStorage.removeItem("token_react");
    localStorage.removeItem("usuario_react");
    setToken("");
    setUsuario(null);
    setDesgloseActual(null);
    setSolicitudActual(null);
  };

  if (!token || !usuario) {
    return <LoginRegistro apiUrl={API_URL} onLoginExitoso={manejarLoginExitoso} />;
  }

  return (
    <div>
      <Navbar usuario={usuario} onCerrarSesion={manejarCerrarSesion} />
      <main className="workspace">
        <FormularioCotizacion
          apiUrl={API_URL}
          onCalcularExito={(desglose, solicitud) => {
            setDesgloseActual(desglose);
            setSolicitudActual(solicitud);
          }}
        />
        <ResumenLiquidacion
          apiUrl={API_URL}
          token={token}
          desglose={desgloseActual}
          solicitud={solicitudActual}
        />
      </main>
    </div>
  );
}
