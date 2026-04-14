import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{
      backgroundColor: "#1a1a2e",
      padding: "1rem 2rem",
      display: "flex",
      gap: "2rem",
      alignItems: "center",
    }}>
      <span style={{ color: "#e94560", fontWeight: "bold", fontSize: "1.2rem" }}>
        E-Commerce
      </span>
      <Link to="/" style={{ color: "white", textDecoration: "none" }}>Produtos</Link>
    </nav>
  );
}