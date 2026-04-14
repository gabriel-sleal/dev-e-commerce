import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/api";
import categoriaImagens from "../api/categoriaImagens";

// O "export" aqui é o que resolve o erro no ProdutoDetalhe
export interface Produto {
  id_produto: string;
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas: number | null;
  comprimento_centimetros: number | null;
  altura_centimetros: number | null;
  largura_centimetros: number | null;
  media_avaliacoes: number | null;
}

export default function Produtos() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [busca, setBusca] = useState("");
  const [categoria, setCategoria] = useState("");
  const navigate = useNavigate();

  const buscarProdutos = async () => {
    try {
      const params: Record<string, string> = {};
      if (busca) params.nome = busca;
      if (categoria) params.categoria = categoria;
      const res = await api.get("/produtos/", { params });
      setProdutos(res.data);
    } catch (error) {
      console.error("Erro ao buscar produtos", error);
    }
  };

  useEffect(() => {
    buscarProdutos();
  }, []);

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
        <h1>Catálogo de Produtos</h1>
        <Link 
          to="/produtos/novo" 
          style={{ padding: "0.8rem 1.5rem", backgroundColor: "#e94560", color: "white", textDecoration: "none", borderRadius: "6px", fontWeight: "bold" }}
        >
          + Novo Produto
        </Link>
      </div>

      <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", flexWrap: "wrap" }}>
        <input
          placeholder="Buscar por nome..."
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          style={{ padding: "0.8rem", borderRadius: "6px", border: "1px solid #333", backgroundColor: "#1a1a2e", color: "white", flex: 1, minWidth: "200px" }}
        />
        <input
          placeholder="Filtrar por categoria..."
          value={categoria}
          onChange={(e) => setCategoria(e.target.value)}
          style={{ padding: "0.8rem", borderRadius: "6px", border: "1px solid #333", backgroundColor: "#1a1a2e", color: "white", flex: 1, minWidth: "200px" }}
        />
        <button
          onClick={buscarProdutos}
          style={{ padding: "0.8rem 2rem", backgroundColor: "#e94560", color: "white", border: "none", borderRadius: "6px", cursor: "pointer", fontWeight: "bold" }}
        >
          Filtrar
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "1.5rem" }}>
        {produtos.map((p) => (
          <div
            key={p.id_produto}
            onClick={() => navigate(`/produtos/${p.id_produto}`)}
            style={{ backgroundColor: "#1a1a2e", color: "white", borderRadius: "10px", cursor: "pointer", border: "1px solid #2a2a4e", overflow: "hidden", transition: "transform 0.2s" }}
            onMouseEnter={(e) => e.currentTarget.style.transform = "translateY(-5px)"}
            onMouseLeave={(e) => e.currentTarget.style.transform = "translateY(0)"}
          >
            <img
              src={categoriaImagens[p.categoria_produto] ?? "https://via.placeholder.com/300x200?text=Sem+Imagem"}
              alt={p.categoria_produto}
              style={{ width: "100%", height: "180px", objectFit: "cover", borderBottom: "2px solid #e94560" }}
              onError={(e) => (e.currentTarget.src = "https://via.placeholder.com/300x200?text=Sem+Imagem")}
            />
            <div style={{ padding: "1.5rem" }}>
              <h3 style={{ marginBottom: "0.5rem", fontSize: "1.1rem", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{p.nome_produto}</h3>
              <p style={{ color: "#888", fontSize: "0.9rem", marginBottom: "1rem" }}>{p.categoria_produto}</p>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: "#f5c518", fontWeight: "bold" }}>⭐ {p.media_avaliacoes ?? "N/A"}</span>
                <span style={{ fontSize: "0.8rem", color: "#aaa" }}>Ver detalhes ➔</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}