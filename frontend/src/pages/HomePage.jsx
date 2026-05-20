import { useContext, useEffect, useMemo, useState } from "react"
import api from "../api/api"
import { UserContext } from "../context/UserContext"

function HomePage() {
  const { currentUser } = useContext(UserContext)
  const [auctions, setAuctions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [categoryFilter, setCategoryFilter] = useState("")
  const [statusFilter, setStatusFilter] = useState("")
  const [bidAmounts, setBidAmounts] = useState({})
  const [createData, setCreateData] = useState({
    name: "",
    description: "",
    category: "",
    starting_price: "",
    start_date: "",
    end_date: ""
  })
  const [formMessage, setFormMessage] = useState("")

  const categories = useMemo(() => {
    const allCategories = auctions.map((auction) => auction.category)
    return [...new Set(allCategories)]
  }, [auctions])

  useEffect(() => {
    fetchAuctions()
  }, [categoryFilter, statusFilter])

  const fetchAuctions = async () => {
    setLoading(true)
    setError(null)

    try {
      const params = {}
      if (categoryFilter) params.category = categoryFilter
      if (statusFilter) params.status = statusFilter

      const response = await api.get("/auctions/", { params })
      setAuctions(response.data)
    } catch (err) {
      setError("Nie udało się pobrać aukcji.")
    } finally {
      setLoading(false)
    }
  }

  const handleBidChange = (auctionId, value) => {
    setBidAmounts((prev) => ({ ...prev, [auctionId]: value }))
  }

  const handleBidSubmit = async (auctionId) => {
    if (!currentUser) {
      alert("Zaloguj się, aby składać oferty.")
      return
    }

    const amount = parseFloat(bidAmounts[auctionId])
    if (!amount || amount <= 0) {
      alert("Wprowadź poprawną kwotę.")
      return
    }

    try {
      await api.post(`/auctions/${auctionId}/bids/`, { amount })
      setFormMessage("Oferta została przyjęta.")
      fetchAuctions()
      setBidAmounts((prev) => ({ ...prev, [auctionId]: "" }))
    } catch (err) {
      setFormMessage("Oferta nie została przyjęta. Sprawdź kwotę i status aukcji.")
    }
  }

  const handleCreateAuction = async (event) => {
    event.preventDefault()
    setFormMessage("")

    if (!currentUser) {
      setFormMessage("Musisz być zalogowany, aby wystawić aukcję.")
      return
    }

    const payload = {
      name: createData.name,
      description: createData.description,
      category: createData.category,
      starting_price: parseFloat(createData.starting_price) || 0,
      start_date: createData.start_date,
      end_date: createData.end_date,
      owner_id: currentUser.id
    }

    if (!payload.name || !payload.description || !payload.category || !payload.start_date || !payload.end_date) {
      setFormMessage("Wypełnij wszystkie pola formularza aukcji.")
      return
    }

    try {
      await api.post("/auctions/", payload)
      setFormMessage("Aukcja została utworzona.")
      setCreateData({
        name: "",
        description: "",
        category: "",
        starting_price: "",
        start_date: "",
        end_date: ""
      })
      fetchAuctions()
    } catch (err) {
      setFormMessage("Nie udało się utworzyć aukcji. Sprawdź dane i spróbuj ponownie.")
    }
  }

  return (
    <main style={styles.container}>
      <section style={styles.intro}>
        <div>
          <h1>Internetowy system aukcyjny</h1>
          <p>Zobacz dostępne aukcje, wystaw przedmiot lub złóż ofertę.</p>
        </div>
      </section>

      <section style={styles.filters}>
        <div>
          <label>
            Kategoria:
            <select value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)}>
              <option value="">Wszystkie</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div>
          <label>
            Status:
            <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              <option value="">Wszystkie</option>
              <option value="active">Active</option>
              <option value="ended">Ended</option>
            </select>
          </label>
        </div>
      </section>

      {error && <div style={styles.error}>{error}</div>}
      {formMessage && <div style={styles.message}>{formMessage}</div>}

      <section style={styles.auctionGrid}>
        {loading ? (
          <p>Ładowanie aukcji...</p>
        ) : auctions.length === 0 ? (
          <p>Brak aukcji do wyświetlenia.</p>
        ) : (
          auctions.map((auction) => (
            <article key={auction.id} style={styles.card}>
              <div style={styles.cardHeader}>
                <h2>{auction.name}</h2>
                <span style={styles.status}>{auction.status}</span>
              </div>
              <p>{auction.description}</p>
              <p>
                <strong>Kategoria:</strong> {auction.category}
              </p>
              <p>
                <strong>Cena wywoławcza:</strong> {auction.starting_price}
              </p>
              <p>
                <strong>Aktualna oferta:</strong> {auction.current_price}
              </p>
              <p>
                <strong>Start:</strong> {new Date(auction.start_date).toLocaleString()}
              </p>
              <p>
                <strong>Koniec:</strong> {new Date(auction.end_date).toLocaleString()}
              </p>
              <p>
                <strong>ID właściciela:</strong> {auction.owner_id}
              </p>

              <div style={styles.bidRow}>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="Kwota"
                  value={bidAmounts[auction.id] || ""}
                  onChange={(e) => handleBidChange(auction.id, e.target.value)}
                  disabled={auction.status === "ended"}
                  style={styles.bidInput}
                />
                <button
                  type="button"
                  onClick={() => handleBidSubmit(auction.id)}
                  disabled={auction.status === "ended"}
                  style={styles.bidButton}
                >
                  Złóż ofertę
                </button>
              </div>
            </article>
          ))
        )}
      </section>

      <section style={styles.createSection}>
        <h2>Wystaw przedmiot na aukcję</h2>
        {currentUser ? (
          <form onSubmit={handleCreateAuction} style={styles.form}>
            <label>
              Nazwa przedmiotu
              <input
                type="text"
                value={createData.name}
                onChange={(e) => setCreateData({ ...createData, name: e.target.value })}
              />
            </label>
            <label>
              Opis
              <textarea
                value={createData.description}
                onChange={(e) => setCreateData({ ...createData, description: e.target.value })}
              />
            </label>
            <label>
              Kategoria
              <input
                type="text"
                value={createData.category}
                onChange={(e) => setCreateData({ ...createData, category: e.target.value })}
              />
            </label>
            <label>
              Cena wywoławcza
              <input
                type="number"
                min="0"
                step="0.01"
                value={createData.starting_price}
                onChange={(e) => setCreateData({ ...createData, starting_price: e.target.value })}
              />
            </label>
            <label>
              Data rozpoczęcia
              <input
                type="datetime-local"
                value={createData.start_date}
                onChange={(e) => setCreateData({ ...createData, start_date: e.target.value })}
              />
            </label>
            <label>
              Data zakończenia
              <input
                type="datetime-local"
                value={createData.end_date}
                onChange={(e) => setCreateData({ ...createData, end_date: e.target.value })}
              />
            </label>
            <button type="submit" style={styles.submitButton}>
              Utwórz aukcję
            </button>
          </form>
        ) : (
          <p>Zaloguj się, aby wystawiać przedmioty i składać oferty.</p>
        )}
      </section>
    </main>
  )
}

const styles = {
  container: {
    padding: "20px",
    maxWidth: "1200px",
    margin: "0 auto"
  },
  intro: {
    marginBottom: "24px"
  },
  filters: {
    display: "flex",
    gap: "20px",
    flexWrap: "wrap",
    marginBottom: "24px",
    justifyContent: "center"
  },
  error: {
    color: "#f87171",
    marginBottom: "12px"
  },
  message: {
    color: "#4ade80",
    marginBottom: "12px"
  },
  auctionGrid: {
    display: "grid",
    gap: "20px",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    marginBottom: "40px"
  },
  card: {
    padding: "18px",
    border: "1px solid var(--border)",
    borderRadius: "10px",
    background: "var(--code-bg)",
    boxShadow: "var(--shadow)",
    color: "var(--text)"
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "10px"
  },
  status: {
    padding: "4px 10px",
    borderRadius: "20px",
    background: "var(--border)",
    textTransform: "capitalize",
    fontSize: "0.9rem"
  },
  bidRow: {
    display: "flex",
    gap: "10px",
    marginTop: "12px",
    alignItems: "center"
  },
  bidInput: {
    flex: 1,
    padding: "10px",
    border: "1px solid var(--border)",
    borderRadius: "8px",
    background: "var(--bg)",
    color: "var(--text)"
  },
  bidButton: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "8px",
    background: "var(--accent)",
    color: "white",
    cursor: "pointer"
  },
  createSection: {
    padding: "20px",
    border: "1px solid var(--border)",
    borderRadius: "10px",
    background: "var(--code-bg)",
    color: "var(--text)"
  },
  form: {
    display: "grid",
    gap: "14px"
  },
  submitButton: {
    width: "fit-content",
    padding: "10px 18px",
    background: "var(--accent)",
    border: "none",
    borderRadius: "8px",
    color: "white",
    cursor: "pointer"
  }
}

export default HomePage
