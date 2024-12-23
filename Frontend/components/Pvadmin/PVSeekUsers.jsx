import React, { useState, useEffect } from "react";
import dbConnect from "../../src/config";

function UserCount() {
  const [totalUsers, setTotalUsers] = useState(null); // Inicializamos el estado en null

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await dbConnect.get("pvadmin/total-usersv2");
        setTotalUsers(response.data.total_users);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {totalUsers !== null ? (
        <p>Total de cuentas: {totalUsers}</p>
      ) : (
        <p>Cargando datos...</p>
      )}
    </div>
  );
}

export default UserCount;
