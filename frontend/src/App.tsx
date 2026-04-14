import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Produtos from "./pages/Produtos";
import ProdutoDetalhe from "./pages/ProdutoDetalhe";
import ProdutoForm from "./pages/ProdutoForm"; // Novo componente!
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Produtos />} />
        <Route path="/produtos/novo" element={<ProdutoForm />} />
        <Route path="/produtos/:id" element={<ProdutoDetalhe />} />
        <Route path="/produtos/editar/:id" element={<ProdutoForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;