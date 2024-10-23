import sqlite3


def get_db_connection():
    # Adicionando um timeout de 10 segundos
    conn = sqlite3.connect("estoque.db", timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    with get_db_connection() as conn:  # Usando um gerenciador de contexto
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL,
                localizacao TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL, -- "entrada" ou "saida"
                quantidade INTEGER NOT NULL,
                data TEXT NOT NULL,
                pedido_id INTEGER,
                observacao TEXT,
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
            """
        )


create_tables()
