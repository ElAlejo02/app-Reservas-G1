// Componente de CLASE (la pregunta 2 del taller: "¿qué son clases en React?").
// Es la forma antigua de escribir componentes: hereda de React.Component,
// guarda el estado en this.state y lo cambia con this.setState().
// Hoy se prefieren los componentes funcionales con useState (como FormularioPasajero).
import { Component } from 'react'

export default class ContadorReservas extends Component {
  constructor(props) {
    super(props) // obligatorio: llama al constructor de la clase madre
    this.state = { noches: 1 }
  }

  // Método de ciclo de vida: se ejecuta una vez cuando el componente aparece en pantalla.
  componentDidMount() {
    document.title = 'Reservas HyD | Pasajeros'
  }

  sumar = () => this.setState({ noches: this.state.noches + 1 })

  restar = () => this.setState({ noches: Math.max(1, this.state.noches - 1) })

  render() {
    const total = this.state.noches * this.props.tarifa
    return (
      <div className="tarjeta contador">
        <span>Cotizador (componente de clase):</span>
        <button className="secundario" onClick={this.restar}>−</button>
        <strong>{this.state.noches} noches</strong>
        <button className="secundario" onClick={this.sumar}>+</button>
        <span>Total: ${total.toLocaleString('es-CO')}</span>
      </div>
    )
  }
}
