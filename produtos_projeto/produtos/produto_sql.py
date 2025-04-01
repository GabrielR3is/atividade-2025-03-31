# SQL para criar a tabela 'produtos' se ela não existir.
# Define as colunas: id (chave primária autoincrementável), nome, preco, estoque.
CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL
)
'''

# SQL para inserir um novo produto.
# Usa placeholders (?) para os valores, prevenindo SQL Injection.
INSERT_PRODUTO = '''
INSERT INTO produtos (nome, preco, estoque)
VALUES (?, ?, ?)
'''

# SQL para selecionar um produto específico pelo seu ID.
SELECT_PRODUTO = '''
SELECT id, nome, preco, estoque
FROM produtos
WHERE id = ?
'''

# SQL para selecionar todos os produtos da tabela.
SELECT_TODOS_PRODUTOS = '''
SELECT id, nome, preco, estoque
FROM produtos
'''

# SQL para atualizar os dados de um produto existente, identificado pelo ID.
UPDATE_PRODUTO = '''
UPDATE produtos
SET nome = ?, preco = ?, estoque = ?
WHERE id = ?
'''

# SQL para excluir um produto da tabela, identificado pelo ID.
DELETE_PRODUTO = '''
DELETE FROM produtos
WHERE id = ?
'''

# SQL para criar a tabela 'comandas' se ela não existir.
# Define as colunas: id (chave primária autoincrementável), produto_id, quantidade.
CREATE_TABLE_COMANDAS = '''
CREATE TABLE IF NOT EXISTS comandas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
'''

# SQL para deletar todos os produtos da tabela 'produtos'.
DELETE_TODOS_PRODUTOS = '''
DELETE FROM produtos
'''
