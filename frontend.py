# type: ignore
import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"


def cadastrar_produto():
    st.header("Cadastro de Produto")
    nome = st.text_input("Nome")
    categoria = st.text_input("Categoria")
    quantidade = st.number_input("Quantidade", min_value=0)
    preco = st.number_input("Preço", min_value=0.0)
    localizacao = st.text_input("Localização")

    if st.button("Cadastrar"):
        produto = {
            "nome": nome,
            "categoria": categoria,
            "quantidade": quantidade,
            "preco": preco,
            "localizacao": localizacao,
        }
        response = requests.post(f"{API_URL}/produtos/", json=produto)
        if response.status_code == 200:
            st.success(response.json()["mensagem"])
        else:
            st.error("Erro ao cadastrar produto.")


def listar_produtos():
    st.header("Lista de Produtos")
    response = requests.get(f"{API_URL}/produtos/")
    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            st.write(
                f"**ID:** {produto['id']}, **Nome:** {produto['nome']}, **Categoria:** {produto['categoria']}, **Quantidade:** {produto['quantidade']}, **Preço:** {produto['preco']}, **Localização:** {produto['localizacao']}"
            )
    else:
        st.error("Erro ao buscar produtos.")


def atualizar_estoque():
    st.header("Atualizar Estoque")
    produto_id = st.number_input("ID do Produto", min_value=1)
    quantidade = st.number_input("Nova Quantidade", min_value=0)

    if st.button("Atualizar"):
        response = requests.put(
            f"{API_URL}/produtos/{produto_id}", json={"quantidade": quantidade}
        )
        if response.status_code == 200:
            st.success(response.json()["mensagem"])
        else:
            st.error("Erro ao atualizar estoque.")


def cadastrar_movimentacao():
    st.header("Cadastro de Movimentação")

    produto_id = st.number_input("ID do Produto", min_value=1)
    quantidade = st.number_input("Quantidade", min_value=1)  # Ajustado para min_value=1
    tipo = st.selectbox("Tipo", options=["entrada", "saida"])
    observacao = st.text_area("Observação")
    pedido_id = st.number_input("ID do Pedido", min_value=1)

    if st.button("Cadastrar Movimentação"):
        movimentacao = {
            "produto_id": produto_id,
            "quantidade": quantidade,
            "tipo": tipo,
            "observacao": observacao,
            "pedido_id": pedido_id,
            "data": datetime.now().isoformat(),  # Adicionando a data
        }
        response = requests.post(f"{API_URL}/movimentacoes", json=movimentacao)

        if response.status_code == 200:
            st.success(response.json()["mensagem"])
        else:
            st.error(f"Erro ao cadastrar movimentação: {response.json()}")


def listar_movimentacoes():
    st.header("Movimentações de Produtos")
    response = requests.get(f"{API_URL}/movimentacoes/")
    if response.status_code == 200:
        movimentacoes = response.json()
        for mov in movimentacoes:
            st.write(
                f"**ID:** {mov['id']}, **Produto ID:** {mov['produto_id']}, **Tipo:** {mov['tipo']}, **Quantidade:** {mov['quantidade']}, **Data:** {mov['data']}"
            )
    else:
        st.error("Erro ao buscar movimentações.")


def listar_movimentacoes_por_pedido():
    st.header("Listar Movimentações por Pedido")
    pedido_id = st.number_input("ID do Pedido", min_value=1)

    if st.button("Buscar Movimentações"):
        response = requests.get(f"{API_URL}/movimentacoes/pedido/{pedido_id}")

        if response.status_code == 200:
            movimentacoes = response.json().get("movimentacoes", [])

            if movimentacoes:
                st.write(f"Movimentações para o Pedido ID: {pedido_id}")
                for mov in movimentacoes:
                    st.write(
                        f"**ID:** {mov['id']}, **Tipo:** {mov['tipo']}, "
                        f"**Quantidade:** {mov['quantidade']}, **Data:** {mov['data']}"
                    )
            else:
                st.write("Nenhuma movimentação encontrada para este pedido.")
        else:
            st.error(f"Erro ao buscar movimentações: {response.text}")


def relatorios():
    st.header("Relatórios de Estoque")
    response = requests.get(f"{API_URL}/relatorios/")

    if response.status_code == 200:
        produtos = response.json()

        if produtos:
            st.write("Todos os produtos em estoque:")
            for produto in produtos:
                st.write(
                    f"**ID:** {produto['id']}, \n**Nome:** {produto['nome']}, \n"
                    f"**Quantidade:** {produto['quantidade']}, \n**Categoria:** {produto.get('categoria', 'N/A')}, \n"
                    f"**Preço:** R$ {produto.get('preco', 0):.2f}\n"
                )
        else:
            st.write("Nenhum produto cadastrado.")
    else:
        st.error(f"Erro ao gerar relatórios: {response.text}")


st.sidebar.title("Menu")
opcao = st.sidebar.selectbox(
    "Escolha uma opção",
    (
        "Cadastrar Produto",
        "Listar Produtos",
        "Atualizar Estoque",
        "Cadastrar Movimentação",
        "Listar Movimentações",
        "Listar Movimentação Por Pedido",
        "Relatórios",
    ),
)

if opcao == "Cadastrar Produto":
    cadastrar_produto()
elif opcao == "Listar Produtos":
    listar_produtos()
elif opcao == "Atualizar Estoque":
    atualizar_estoque()
elif opcao == "Cadastrar Movimentação":
    cadastrar_movimentacao()
elif opcao == "Listar Movimentações":
    listar_movimentacoes()
elif opcao == "Listar Movimentação Por Pedido":
    listar_movimentacoes_por_pedido()
elif opcao == "Relatórios":
    relatorios()
