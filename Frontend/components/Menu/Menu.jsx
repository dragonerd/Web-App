import React from "react";
import { Link } from "react-router-dom";

export const Menu = () => (
  <nav className="navbar navbar-expand-lg bg-body-tertiary">
    <div className="container-fluid">
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav">
          <li className="nav-item">
            <Link className="nav-link active" aria-current="page" to="/">
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="#">
              Login
            </Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/notices">
              Noticias
            </Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/eventos">
              Eventos
            </Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/About">
              Contacto
            </Link>
          </li>
        </ul>
      </div>
      <h1>PROYECTO ELO</h1>
    </div>
  </nav>
);
