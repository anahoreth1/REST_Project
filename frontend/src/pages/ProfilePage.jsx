import { useContext, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api/api"
import { UserContext } from "../context/UserContext"

function ProfilePage() {
    const { currentUser, setCurrentUser } = useContext(UserContext)
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [message, setMessage] = useState(null)
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        if (!currentUser) {
            navigate("/login")
            return
        }
        setName(currentUser.name || "")
        setEmail(currentUser.email || "")
    }, [currentUser, navigate])

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        setMessage(null);

        if (!name || !email) {
            setError("Wypełnij imię i email.");
            return;
        }

        const payload = {
            name,
            email,
        };

        if (password.trim()) {
            payload.password = password;
        }

        try {
            const response = await api.put(
                `/users/${currentUser.id}/`,
                payload
            );

            setCurrentUser(response.data);
            localStorage.setItem("user", JSON.stringify(response.data));

            setPassword("");
            setMessage("Dane konta zostały zaktualizowane.");

        } catch (err) {
            const status = err.response?.status;

            if (status === 401) {
                setError("Brak autoryzacji.");
            } else if (status === 400) {
                setError("Nieprawidłowe dane.");
            } else {
                setError(
                    err.response?.data?.message ||
                    "Nie udało się zaktualizować profilu."
                );
            }
        }
    }

    const handleDelete = async () => {
        const confirmed = window.confirm(
            "Na pewno usunąć konto? Ta operacja jest nieodwracalna."
        );
        if (!confirmed) return;

        try {
            await api.delete(`/users/${currentUser.id}/`);

            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            localStorage.removeItem("user");

            setCurrentUser(null);
            navigate("/");

        } catch (err) {
            const status = err.response?.status;

            if (status === 401) {
                setError("Brak autoryzacji.");
            } else {
                setError("Nie udało się usunąć konta. Spróbuj ponownie.");
            }
        }
    }

    if (!currentUser) {
        return null
    }

    return (
        <div style={styles.container}>
            <h2>Mój profil</h2>
            <p>Edytuj dane konta lub usuń konto.</p>

            <form onSubmit={handleSubmit} style={styles.form}>
                <input
                    type="text"
                    placeholder="Imię"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    style={styles.input}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={styles.input}
                />
                <input
                    type="password"
                    placeholder="Nowe hasło (opcjonalnie)"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={styles.input}
                />

                <button type="submit" style={styles.button}>
                    Zapisz zmiany
                </button>
            </form>

            {message && <div style={styles.message}>{message}</div>}
            {error && <div style={styles.error}>{error}</div>}

            <div style={styles.deleteBlock}>
                <button type="button" style={styles.deleteButton} onClick={handleDelete}>
                    Usuń konto
                </button>
            </div>
        </div>
    )
}

const styles = {
    container: {
        padding: "20px",
        maxWidth: "520px",
        margin: "0 auto",
        textAlign: "left"
    },
    form: {
        display: "grid",
        gap: "12px",
        marginTop: "12px"
    },
    input: {
        background: "var(--code-bg)",
        color: "var(--text)",
        border: "1px solid var(--border)",
        borderRadius: "10px",
        padding: "10px"
    },
    button: {
        background: "var(--accent)",
        color: "white",
        border: "none",
        borderRadius: "10px",
        padding: "10px 16px",
        cursor: "pointer"
    },
    deleteBlock: {
        marginTop: "20px"
    },
    deleteButton: {
        background: "#ef4444",
        color: "white",
        border: "none",
        borderRadius: "10px",
        padding: "10px 16px",
        cursor: "pointer"
    },
    message: {
        color: "#4ade80",
        marginTop: "12px"
    },
    error: {
        color: "#f87171",
        marginTop: "12px"
    }
}

export default ProfilePage
