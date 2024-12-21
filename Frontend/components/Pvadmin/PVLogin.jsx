import React, { useState } from "react";
import axios from "axios";

export function PvadminLogin() {
  const [pvadmin_email, setPvadmin_Email] = useState("");
  const [pvadmin_password, setPvadmin_Password] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/pvadmin/loginv2",
        {
          pvadmin_email,
          pvadmin_password,
        }
      );
      const loginData = response.data.login_data;
      console.log(loginData);

      localStorage.setItem("userData", JSON.stringify(loginData));

      // Redirigir al usuario
      window.location.href = "http://127.0.0.1:5000/pvadmin/dashboardv2";
    } catch (error) {
      // Manejar errores
    }
  };

  return (
    <div>
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
        <div>
          <label htmlFor="pvadmin_email">Email:</label>
          <input
            type="email"
            id="pvadmin_email"
            value={pvadmin_email}
            onChange={(e) => setPvadmin_Email(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="pvadmin_password">Contraseña:</label>
          <input
            type="password"
            id="pvadmin_password"
            value={pvadmin_password}
            onChange={(e) => setPvadmin_Password(e.target.value)}
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>
  );
}

export default PvadminLogin;
