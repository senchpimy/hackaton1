import { useState, useEffect } from "react";

export const useAuth = () => {
    const [users, setUsers] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");

    // Función para cargar los usuarios
    const loadUsers = async () => {
        try {
            const response = await fetch("./publi/user.json"); // Asegúrate de que la ruta sea correcta
            if (!response.ok) throw new Error("Error al cargar los usuarios");
            const data = await response.json();
            setUsers(data);
        } catch (error) {
            setErrorMessage("Error al cargar los datos de usuarios.");
        }
    };

    useEffect(() => {
        loadUsers();
    }, []);

    // Función para autenticar
    const authenticate = (username, password) => {
        if (!username || !password) {
            setErrorMessage("Por favor, completa todos los campos.");
            return false;
        }

        const userExists = users.some(user => user.username === username && user.password === password);

        if (userExists) {
            setErrorMessage("");
            return true; // Usuario autenticado
        } else {
            setErrorMessage("Credenciales incorrectas.");
            return false;
        }
    };

    return { authenticate, errorMessage };
};
