import { useState, useEffect } from "react";

function UserProfile() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const storedData = localStorage.getItem("userData");
    if (storedData) {
      setUserData(JSON.parse(storedData));
    }
  }, []);

  return (
    <div>
      <h1>Bienvenido, {userData?.email}!</h1>
      {/* Mostrar otros datos del usuario */}
    </div>
  );
}
