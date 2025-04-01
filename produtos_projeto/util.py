from contextlib import contextmanager
import sqlite3

# Define o nome padrão do arquivo do banco de dados
DB_NAME = 'dados.db'

@contextmanager
def get_db_connection(db_name=DB_NAME):
    """
    Gerenciador de contexto para conexões com o banco de dados SQLite.
    Garante que a conexão seja fechada e as alterações commitadas.
    """
    conn = None # Inicializa conn como None
    try:
        # Estabelece a conexão com o banco de dados
        conn = sqlite3.connect(db_name)
        # Disponibiliza a conexão para ser usada dentro do bloco 'with'
        yield conn
    finally:
        # Este bloco é executado sempre, mesmo se ocorrerem erros
        if conn:
            # Confirma (commita) as transações pendentes
            conn.commit()
            # Fecha a conexão com o banco de dados
            conn.close()
