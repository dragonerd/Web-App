import React, { useState, useEffect } from "react";
import dbConnect from "../../src/config";
import UserCount from "./PVSeekUsers";

export function UsersList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await dbConnect.get("/pvadmin/all-usersv2");
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      <h1>Base de datos</h1>
      <h2>
        <UserCount />
      </h2>

      {users.length > 0 ? (
        <div class="container mt-3">
          <table className="table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Full Name</th>
                <th>Status</th>
                <th>Discipline</th>
                <th>Intentos Validacion Email</th>
              </tr>
            </thead>
            <tbody>
              {users.map((item) => (
                <tr key={item.id}>
                  <td>{item.username}</td>
                  <td>{item.email}</td>
                  <td>
                    {item.fname} {item.lname}
                  </td>
                  <td>{item.status}</td>

                  <td>{item.discipline}</td>
                  <td>{item.trysend}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>Cargando usuarios...</p>
      )}
    </div>
  );
}
