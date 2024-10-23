# type: ignore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database


app = FastAPI()


class Produto(BaseModel):
    nome: str
    categoria: str
    quantidade: int
    preco: float
    localizacao: str


class Movimentacao(BaseModel):
    produto_id: int
    tipo: str  # "entrada" ou "saida"
    quantidade: int
    data: str  # Ou datetime, se você quiser fazer a validação automática
    pedido_id: int = None  # Opcional
    observacao: str = None  # Opcional


class AtualizarEstoque(BaseModel):
    quantidade: int


@app.post("/produtos/")
def cadastrar_produto(produto: Produto):
    conn = database.get_db_connection()
    conn.execute(
        """
        INSERT INTO produtos (nome, categoria, quantidade, preco, localizacao)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            produto.nome,
            produto.categoria,
            produto.quantidade,
            produto.preco,
            produto.localizacao,
        ),
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Produto cadastrado com sucesso!"}


@app.get("/produtos/")
def listar_produtos():
    conn = database.get_db_connection()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return [dict(produto) for produto in produtos]


@app.put("/produtos/{produto_id}")
def atualizar_estoque(produto_id: int, estoque: AtualizarEstoque):
    conn = database.get_db_connection()

    # Verificar se o produto existe
    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ?", (produto_id,)
    ).fetchone()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    # Atualizar a quantidade
    try:
        conn.execute(
            f"""
            UPDATE produtos SET quantidade = {estoque.quantidade} WHERE id = {produto_id}
            """,
        )  # Acessa a quantidade corretamente
        print("executado a suposta atualização.")
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return {"mensagem": "Estoque atualizado com sucesso!"}


@app.post("/movimentacoes")
def cadastrar_movimentacao(movimentacao: Movimentacao):
    conn = database.get_db_connection()
    try:
        conn.execute(
            "INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, pedido_id, observacao) VALUES (?, ?, ?, ?, ?, ?)",
            (
                movimentacao.produto_id,
                movimentacao.tipo,
                movimentacao.quantidade,
                movimentacao.data,
                movimentacao.pedido_id,
                movimentacao.observacao,
            ),
        )
        conn.commit()
        return {"mensagem": "Movimentação cadastrada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


@app.get("/movimentacoes/")
def listar_movimentacoes():
    conn = database.get_db_connection()
    movimentacoes = conn.execute("SELECT * FROM movimentacoes").fetchall()
    conn.close()
    return [dict(movimentacao) for movimentacao in movimentacoes]


@app.get("/movimentacoes/pedido/{pedido_id}")
def listar_movimentacoes_por_pedido(pedido_id: int):
    conn = database.get_db_connection()

    movimentacoes = conn.execute(
        "SELECT * FROM movimentacoes WHERE pedido_id = ?", (pedido_id,)
    ).fetchall()

    conn.close()
    return {"movimentacoes": [dict(row) for row in movimentacoes]}


@app.get("/relatorios/")
def relatorios():
    try:
        conn = database.get_db_connection()
        produtos = conn.execute(
            "SELECT * FROM produtos"
        ).fetchall()  # Pega todos os produtos
        conn.close()
        return [dict(produto) for produto in produtos]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )  # Tratamento de erro genérico
