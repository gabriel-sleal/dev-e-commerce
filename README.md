# Sistema de Gerenciamento de E-Commerce

API REST para gerenciamento de produtos, pedidos, consumidores e vendedores.

## Tecnologias

- **Frontend:** Vite + React + TypeScript
- **Backend:** FastAPI (Python)
- **Banco de dados:** SQLite + SQLAlchemy + Alembic

## Pré-requisitos

- Python 3.11+
- Node.js 18+

## Como executar

### Backend

1. Entre na pasta do backend:
```bash
cd backend
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o arquivo de ambiente:
```bash
cp .env.example .env
```

5. Rode as migrations:
```bash
alembic upgrade head
```

6. Popular o banco de dados:
```bash
python seed.py
```

7. Inicie o servidor:
```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`  
Documentação Swagger em `http://localhost:8000/docs`

### Frontend

1. Entre na pasta do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Inicie o servidor:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## Endpoints

### Produtos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/produtos/` | Listar produtos |
| GET | `/produtos/{id}` | Buscar produto |
| POST | `/produtos/` | Criar produto |
| PUT | `/produtos/{id}` | Atualizar produto |
| DELETE | `/produtos/{id}` | Remover produto |

### Consumidores
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/consumidores/` | Listar consumidores |
| GET | `/consumidores/{id}` | Buscar consumidor |
| POST | `/consumidores/` | Criar consumidor |
| PUT | `/consumidores/{id}` | Atualizar consumidor |
| DELETE | `/consumidores/{id}` | Remover consumidor |

### Vendedores
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/vendedores/` | Listar vendedores |
| GET | `/vendedores/{id}` | Buscar vendedor |
| POST | `/vendedores/` | Criar vendedor |
| PUT | `/vendedores/{id}` | Atualizar vendedor |
| DELETE | `/vendedores/{id}` | Remover vendedor |

### Pedidos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/pedidos/` | Listar pedidos |
| GET | `/pedidos/{id}` | Buscar pedido |
| POST | `/pedidos/` | Criar pedido |
| PUT | `/pedidos/{id}` | Atualizar pedido |
| DELETE | `/pedidos/{id}` | Remover pedido |