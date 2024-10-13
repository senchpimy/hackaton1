import React from 'react';
import "../assets/styleHome.css";



const HomePage = () => {
    return (
        <div>
            <header>
                <nav>
                    <div className="menu-icon"><i className="fas fa-bars"></i></div>
                    <div className="user-icon"><i className="fas fa-user"></i></div>
                </nav>
            </header>

            <main>
                <div className="saludo">
                    <h1>¡Hola Carlos, Buenos Días!</h1>
                    <p>¿Qué operación necesitas realizar?</p>
                </div>

                <div className="textRecom">
                    <h2>¿Necesitas alguna recomendación?</h2>
                </div>

                <div className="icon-container">
                    <div className="icon-box">
                        <img src="media/kac.png" alt="Transferencia a Leonardo" />
                        <p>Transferencia a Leonardo</p>
                    </div>
                    <div className="icon-box">
                        <img src="media/kac.png" alt="Compra en MacDonald's" />
                        <p>Compra en MacDonald's</p>
                    </div>
                    <div className="icon-box">
                        <img src="media/kac.png" alt="Recarga Tarjeta MI" />
                        <p>Recarga Tarjeta MI</p>
                    </div>
                    <div className="icon-box">
                        <img src="media/kac.png" alt="Compra en Amazon" />
                        <p>Recarga Tarjeta MI</p>
                    </div>
                    <div className="icon-box">
                        <img src="media/kac.png" alt="Paga en TicketMaster" />
                        <p>Paga boletos en TicketMaster</p>
                    </div>
                    <div className="icon-box">
                        <img src="media/kac.png" alt="Paga en TicketMaster" />
                        <p>Paga boletos en TicketMaster</p>
                    </div>
                </div>

                <div className="input-container">
                    <div className="circle"></div>
                    <input type="text" id="peticionInput" placeholder="Escribe tu petición..." />
                    <button id="enviarBtn">Enviar</button>
                </div>
            </main>
        </div>
    );
};

export default HomePage;
