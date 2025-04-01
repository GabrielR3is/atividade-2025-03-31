from typing import List, Optional
from produtos.produto import Produto  # Importa a classe de domínio
from produtos import produto_sql as sql # Importa as constantes SQL
from util import get_db_connection     # Importa o gerenciador de conexão

class ProdutoRepo:
    """
    Repositório para gerenciar operações CRUD (Create, Read, Update, Delete)
    para a entidade Produto no banco de dados.
    """
    def __init__(self):
        """Inicializa o repositório e garante que a tabela de produtos exista."""
        self._criar_tabela()
        self._criar_tabela_comandas()

    def _criar_tabela(self):
        """Método privado para criar a tabela 'produtos' se ela não existir."""
        try:
            # Usa o gerenciador de contexto para obter uma conexão segura
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL para criar a tabela
                cursor.execute(sql.CREATE_TABLE)
                # Commit e close são feitos automaticamente pelo context manager
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")
            # Considerar relançar a exceção ou tratar de forma mais robusta
    
    def _criar_tabela_comandas(self):
        """Método privado para criar a tabela 'comandas' se ela não existir."""
        try:
            # Usa o gerenciador de contexto para obter uma conexão segura
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL para criar a tabela
                cursor.execute(sql.CREATE_TABLE_COMANDAS)
                # Commit e close são feitos automaticamente pelo context manager
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela comandas: {e}")
            # Considerar relançar a exceção ou tratar de forma mais robusta

    def adicionar(self, produto: Produto) -> Optional[int]:
        """
        Adiciona um novo produto ao banco de dados.
        Recebe um objeto Produto (validado pelo Pydantic).
        Retorna o ID do produto inserido ou None em caso de erro.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL de inserção, passando os dados do produto
                cursor.execute(sql.INSERT_PRODUTO, (produto.nome, produto.preco, produto.estoque))
                # Retorna o ID da última linha inserida
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao adicionar produto: {e}")
            return None # Retorna None para indicar falha

    def obter(self, produto_id: int) -> Optional[Produto]:
        """
        Busca um produto no banco de dados pelo seu ID.
        Retorna um objeto Produto se encontrado, caso contrário, retorna None.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL de seleção por ID
                cursor.execute(sql.SELECT_PRODUTO, (produto_id,))
                # Recupera a primeira linha do resultado
                row = cursor.fetchone()
                if row:
                    # Cria e retorna um objeto Produto com os dados do banco
                    return Produto(id=row[0], nome=row[1], preco=row[2], estoque=row[3])
                return None # Retorna None se nenhum produto for encontrado com o ID
        except sqlite3.Error as e:
            print(f"Erro ao obter produto {produto_id}: {e}")
            return None

    def obter_todos(self) -> List[Produto]:
        """
        Busca todos os produtos cadastrados no banco de dados.
        Retorna uma lista de objetos Produto. Se não houver produtos, retorna uma lista vazia.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL para selecionar todos os produtos
                cursor.execute(sql.SELECT_TODOS_PRODUTOS)
                # Recupera todas as linhas do resultado
                rows = cursor.fetchall()
                # Cria uma lista de objetos Produto a partir das linhas retornadas
                return [Produto(id=row[0], nome=row[1], preco=row[2], estoque=row[3]) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao obter todos os produtos: {e}")
            return [] # Retorna lista vazia em caso de erro

    def atualizar(self, produto: Produto) -> bool:
        """
        Atualiza os dados de um produto existente no banco de dados.
        Recebe um objeto Produto com os dados atualizados (incluindo o ID).
        Retorna True se a atualização foi bem-sucedida (pelo menos uma linha afetada),
        False caso contrário (ex: produto com o ID não encontrado).
        """
        # Garante que o produto tenha um ID para atualização
        if produto.id is None:
            print("Erro: Produto sem ID não pode ser atualizado.")
            return False
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL de atualização
                cursor.execute(sql.UPDATE_PRODUTO, (produto.nome, produto.preco, produto.estoque, produto.id))
                # Verifica se alguma linha foi realmente modificada
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao atualizar produto {produto.id}: {e}")
            return False

    def excluir(self, produto_id: int) -> bool:
        """
        Exclui um produto do banco de dados pelo seu ID.
        Retorna True se a exclusão foi bem-sucedida (pelo menos uma linha afetada),
        False caso contrário (ex: produto com o ID não encontrado).
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL de exclusão
                cursor.execute(sql.DELETE_PRODUTO, (produto_id,))
                # Verifica se alguma linha foi realmente excluída
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao excluir produto {produto_id}: {e}")
            return False

    def excluir_todos(self) -> bool:
        """
        Exclui todos os produtos do banco de dados.
        Retorna True se a exclusão foi bem-sucedida (pelo menos uma linha afetada),
        False caso contrário.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Executa o SQL de exclusão
                cursor.execute(sql.DELETE_TODOS_PRODUTOS)
                # Verifica se alguma linha foi realmente excluída
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao excluir todos os produtos: {e}")
            return False
