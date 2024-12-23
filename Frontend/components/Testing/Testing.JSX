import React, { useState, useEffect } from "react";
import axios from "axios";

function Testing() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get("/training/justdance")
      .then((response) => {
        setData(response.data);
        console.log("Datos recibidos:", response.data); // Log para verificar los datos
      })
      .catch((error) => {
        console.error("Error al obtener los datos:", error);
      });
  }, []);

  return <div>{data ? <p>Los datos son: {data}</p> : <p>Cargando...</p>}</div>;
}
