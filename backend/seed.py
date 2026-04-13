import csv
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.consumidor import Consumidor
from app.models.produto import Produto
from app.models.vendedor import Vendedor
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido

Base.metadata.create_all(bind=engine)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def ler_csv(nome):
    caminho = os.path.join(DATA_DIR, nome)
    with open(caminho, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def seed_consumidores(db):
    print("Populando consumidores...")
    rows = ler_csv("dim_consumidores.csv")
    for r in rows:
        if not db.query(Consumidor).filter_by(id_consumidor=r["id_consumidor"]).first():
            db.add(Consumidor(
                id_consumidor=r["id_consumidor"],
                prefixo_cep=r["prefixo_cep"],
                nome_consumidor=r["nome_consumidor"],
                cidade=r["cidade"],
                estado=r["estado"],
            ))
    db.commit()
    print(f"  {len(rows)} consumidores inseridos.")


def seed_produtos(db):
    print("Populando produtos...")
    rows = ler_csv("dim_produtos.csv")
    for r in rows:
        if not db.query(Produto).filter_by(id_produto=r["id_produto"]).first():
            db.add(Produto(
                id_produto=r["id_produto"],
                nome_produto=r["nome_produto"],
                categoria_produto=r["categoria_produto"],
                peso_produto_gramas=float(r["peso_produto_gramas"]) if r.get("peso_produto_gramas") else None,
                comprimento_centimetros=float(r["comprimento_centimetros"]) if r.get("comprimento_centimetros") else None,
                altura_centimetros=float(r["altura_centimetros"]) if r.get("altura_centimetros") else None,
                largura_centimetros=float(r["largura_centimetros"]) if r.get("largura_centimetros") else None,
            ))
    db.commit()
    print(f"  {len(rows)} produtos inseridos.")


def seed_vendedores(db):
    print("Populando vendedores...")
    rows = ler_csv("dim_vendedores.csv")
    for r in rows:
        if not db.query(Vendedor).filter_by(id_vendedor=r["id_vendedor"]).first():
            db.add(Vendedor(
                id_vendedor=r["id_vendedor"],
                nome_vendedor=r["nome_vendedor"],
                prefixo_cep=r["prefixo_cep"],
                cidade=r["cidade"],
                estado=r["estado"],
            ))
    db.commit()
    print(f"  {len(rows)} vendedores inseridos.")


def seed_pedidos(db):
    print("Populando pedidos...")
    rows = ler_csv("fat_pedidos.csv")
    from datetime import datetime

    def parse_dt(val):
        if not val:
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
        except:
            return None

    def parse_date(val):
        if not val:
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except:
            return None

    for r in rows:
        if not db.query(Pedido).filter_by(id_pedido=r["id_pedido"]).first():
            db.add(Pedido(
                id_pedido=r["id_pedido"],
                id_consumidor=r["id_consumidor"],
                status=r["status"],
                pedido_compra_timestamp=parse_dt(r.get("pedido_compra_timestamp")),
                pedido_entregue_timestamp=parse_dt(r.get("pedido_entregue_timestamp")),
                data_estimada_entrega=parse_date(r.get("data_estimada_entrega")),
                tempo_entrega_dias=float(r["tempo_entrega_dias"]) if r.get("tempo_entrega_dias") else None,
                tempo_entrega_estimado_dias=float(r["tempo_entrega_estimado_dias"]) if r.get("tempo_entrega_estimado_dias") else None,
                diferenca_entrega_dias=float(r["diferenca_entrega_dias"]) if r.get("diferenca_entrega_dias") else None,
                entrega_no_prazo=r.get("entrega_no_prazo"),
            ))
    db.commit()
    print(f"  {len(rows)} pedidos inseridos.")


def seed_itens(db):
    print("Populando itens de pedido...")
    rows = ler_csv("fat_itens_pedidos.csv")
    inseridos = 0
    for r in rows:
        if not db.query(ItemPedido).filter_by(id_pedido=r["id_pedido"], id_item=int(r["id_item"])).first():
            db.add(ItemPedido(
                id_pedido=r["id_pedido"],
                id_item=int(r["id_item"]),
                id_produto=r["id_produto"],
                id_vendedor=r["id_vendedor"],
                preco_BRL=float(r["preco_BRL"]) if r.get("preco_BRL") else 0.0,
                preco_frete=float(r["preco_frete"]) if r.get("preco_frete") else 0.0,
            ))
            inseridos += 1
    db.commit()
    print(f"  {inseridos} itens inseridos.")


def seed_avaliacoes(db):
    print("Populando avaliações...")
    rows = ler_csv("fat_avaliacoes_pedidos.csv")
    from datetime import datetime

    def parse_dt(val):
        if not val:
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
        except:
            return None

    inseridos = 0
    for r in rows:
        if not db.query(AvaliacaoPedido).filter_by(id_avaliacao=r["id_avaliacao"]).first():
            try:
                db.add(AvaliacaoPedido(
                    id_avaliacao=r["id_avaliacao"],
                    id_pedido=r["id_pedido"],
                    avaliacao=int(r["avaliacao"]),
                    titulo_comentario=r.get("titulo_comentario"),
                    comentario=r.get("comentario"),
                    data_comentario=parse_dt(r.get("data_comentario")),
                    data_resposta=parse_dt(r.get("data_resposta")),
                ))
                db.commit()
                inseridos += 1
            except Exception:
                db.rollback()

    print(f"  {inseridos} avaliações inseridas.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_consumidores(db)
        seed_produtos(db)
        seed_vendedores(db)
        seed_pedidos(db)
        seed_itens(db)
        seed_avaliacoes(db)
        print("\nSeed concluído com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        db.rollback()
    finally:
        db.close()