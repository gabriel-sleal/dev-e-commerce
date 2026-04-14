import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/api";

export default function ProdutoForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditing = Boolean(id);

  const [formData, setFormData] = useState({
    id_produto: "", 
    nome_produto: "",
    categoria_produto: "",
    peso_produto_gramas: "",
    comprimento_centimetros: "",
    altura_centimetros: "",
    largura_centimetros: "",
  });

  useEffect(() => {
    if (isEditing) {
      api.get(`/produtos/${id}`).then((res) => {
        const p = res.data;
        setFormData({
          id_produto: p.id_produto,
          nome_produto: p.nome_produto,
          categoria_produto: p.categoria_produto,
          peso_produto_gramas: p.peso_produto_gramas ?? "",
          comprimento_centimetros: p.comprimento_centimetros ?? "",
          altura_centimetros: p.altura_centimetros ?? "",
          largura_centimetros: p.largura_centimetros ?? "",
        });
      });
    } else {
      setFormData(prev => ({ ...prev, id_produto: `prod-${Math.floor(Math.random() * 10000)}` }));
    }
  }, [id, isEditing]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const payload = {
      ...formData,
      peso_produto_gramas: formData.peso_produto_gramas ? parseFloat(formData.peso_produto_gramas as string) : null,
      comprimento_centimetros: formData.comprimento_centimetros ? parseFloat(formData.comprimento_centimetros as string) : null,
      altura_centimetros: formData.altura_centimetros ? parseFloat(formData.altura_centimetros as string) : null,
      largura_centimetros: formData.largura_centimetros ? parseFloat(formData.largura_centimetros as string) : null,
    };

    try {
      if (isEditing) {
        await api.put(`/produtos/${id}`, payload);
        alert("Produto atualizado!");
      } else {
        await api.post("/produtos/", payload);
        alert("Produto criado!");
      }
      navigate("/");
    } catch (error) {
      alert("Erro ao salvar produto. Verifique o console.");
      console.error(error);
    }
  };

  const inputStyle = { width: "100%", padding: "0.8rem", marginBottom: "1rem", borderRadius: "6px", border: "1px solid #333", backgroundColor: "#1a1a2e", color: "white", boxSizing: "border-box" as const };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto", color: "white" }}>
      <button onClick={() => navigate(-1)} style={{ marginBottom: "2rem", padding: "0.5rem 1rem", cursor: "pointer", borderRadius: "6px", border: "1px solid #e94560", backgroundColor: "transparent", color: "#e94560" }}>
        Cancelar
      </button>

      <h2>{isEditing ? "Editar Produto" : "Novo Produto"}</h2>
      
      <form onSubmit={handleSubmit} style={{ backgroundColor: "#1a1a2e", padding: "2rem", borderRadius: "12px", border: "1px solid #2a2a4e", marginTop: "1rem" }}>
        
        <label>ID do Produto (Gerado)</label>
        <input name="id_produto" value={formData.id_produto} disabled style={{ ...inputStyle, opacity: 0.5 }} />

        <label>Nome do Produto *</label>
        <input name="nome_produto" value={formData.nome_produto} onChange={handleChange} required style={inputStyle} />

        <label>Categoria *</label>
        <input name="categoria_produto" value={formData.categoria_produto} onChange={handleChange} required style={inputStyle} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
          <div>
            <label>Peso (g)</label>
            <input type="number" step="0.01" name="peso_produto_gramas" value={formData.peso_produto_gramas} onChange={handleChange} style={inputStyle} />
          </div>
          <div>
            <label>Comprimento (cm)</label>
            <input type="number" step="0.01" name="comprimento_centimetros" value={formData.comprimento_centimetros} onChange={handleChange} style={inputStyle} />
          </div>
          <div>
            <label>Altura (cm)</label>
            <input type="number" step="0.01" name="altura_centimetros" value={formData.altura_centimetros} onChange={handleChange} style={inputStyle} />
          </div>
          <div>
            <label>Largura (cm)</label>
            <input type="number" step="0.01" name="largura_centimetros" value={formData.largura_centimetros} onChange={handleChange} style={inputStyle} />
          </div>
        </div>

        <button type="submit" style={{ width: "100%", padding: "1rem", backgroundColor: "#e94560", color: "white", border: "none", borderRadius: "6px", cursor: "pointer", fontWeight: "bold", marginTop: "1rem", fontSize: "1.1rem" }}>
          {isEditing ? "Salvar Alterações" : "Cadastrar Produto"}
        </button>
      </form>
    </div>
  );
}