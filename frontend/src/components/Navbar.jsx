import { Link } from "react-router-dom"

function Navbar() {
  return (
    <nav style={styles.nav}>
      <h2>Auction App</h2>

      <div style={styles.links}>
        <Link to="/">Home</Link>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </div>
    </nav>
  )
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    padding: "20px",
    background: "#eeeeee"
  },
  links: {
    display: "flex",
    gap: "15px"
  }
}

export default Navbar
