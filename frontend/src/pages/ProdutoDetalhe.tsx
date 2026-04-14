import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import api from "../api/api";
import type { Produto } from "./Produtos";

export default function ProdutoDetalhe() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [produto, setProduto] = useState<Produto | null>(null);

  useEffect(() => {
    api.get(`/produtos/${id}`).then((res) => setProduto(res.data)).catch(err => console.error(err));
  }, [id]);

  const handleDelete = async () => {
    const confirm = window.confirm("Tem certeza que deseja excluir este produto?");
    if (confirm) {
      try {
        await api.delete(`/produtos/${id}`);
        alert("Produto excluído com sucesso!");
        navigate("/");
      } catch (error) {
        alert("Erro ao excluir produto.");
        console.error(error);
      }
    }
  };

  if (!produto) return <p style={{ padding: "2rem", color: "white" }}>Carregando produto...</p>;

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <button onClick={() => navigate(-1)} style={{ marginBottom: "2rem", padding: "0.5rem 1rem", cursor: "pointer", borderRadius: "6px", border: "1px solid #e94560", backgroundColor: "transparent", color: "#e94560" }}>
        ← Voltar ao Catálogo
      </button>

      <div style={{ backgroundColor: "#1a1a2e", color: "white", padding: "2.5rem", borderRadius: "12px", border: "1px solid #2a2a4e" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1rem" }}>
          <div>
            <h1 style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>{produto.nome_produto}</h1>
            <span style={{ backgroundColor: "#e94560", padding: "0.3rem 0.8rem", borderRadius: "20px", fontSize: "0.9rem" }}>{produto.categoria_produto}</span>
          </div>
          <h2 style={{ color: "#f5c518", margin: 0 }}>⭐ {produto.media_avaliacoes ?? "Sem avaliações"}</h2>
        </div>

        <hr style={{ borderColor: "#2a2a4e", margin: "2rem 0" }} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem" }}>
          <div>
            <h3 style={{ marginBottom: "1rem", color: "#aaa" }}>Dimensões e Peso</h3>
            <ul style={{ listStyle: "none", padding: 0, lineHeight: "2" }}>
              <li><strong>Peso:</strong> {produto.peso_produto_gramas ?? "N/A"} g</li>
              <li><strong>Comprimento:</strong> {produto.comprimento_centimetros ?? "N/A"} cm</li>
              <li><strong>Altura:</strong> {produto.altura_centimetros ?? "N/A"} cm</li>
              <li><strong>Largura:</strong> {produto.largura_centimetros ?? "N/A"} cm</li>
            </ul>
          </div>
          
          <div>
            <h3 style={{ marginBottom: "1rem", color: "#aaa" }}>Desempenho (Requisito)</h3>
            <p style={{ fontSize: "0.9rem", color: "#888" }}>
              *Para ver as vendas e comentários exatos deste produto, as rotas do backend precisarão ser expandidas futuramente.*
            </p>
          </div>
        </div>

        <div style={{ display: "flex", gap: "1rem", marginTop: "3rem" }}>
          <Link to={`/produtos/editar/${produto.id_produto}`} style={{ flex: 1, textAlign: "center", padding: "1rem", backgroundColor: "#4caf50", color: "white", textDecoration: "none", borderRadius: "6px", fontWeight: "bold" }}>
            Editar Produto
          </Link>
          <button onClick={handleDelete} style={{ flex: 1, padding: "1rem", backgroundColor: "#f44336", color: "white", border: "none", borderRadius: "6px", cursor: "pointer", fontWeight: "bold" }}>
            Excluir Produto
          </button>
        </div>
      </div>
    </div>
  );
}