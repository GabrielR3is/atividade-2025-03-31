from pydantic import ValidationError
from tabulate import tabulate
from produtos.produto_repo import ProdutoRepo
from produtos.produto import Produto

# Lista para armazenar as comandas
comandas = []

def exibir_cardapio(repo: ProdutoRepo):
    """Exibe o cardápio de produtos."""
    print("\n--- Cardápio ---")
    produtos = repo.obter_todos()
    if produtos:
        tabela = [[p.id, p.nome, f"R$ {p.preco:.2f}"] for p in produtos]
        cabecalhos = ["ID", "Nome", "Preço"]
        print(tabulate(tabela, headers=cabecalhos, tablefmt="grid", numalign="right", stralign="left"))
    else:
        print("Nenhum item cadastrado no cardápio.")

def listar_comandas():
    """Lista as comandas em aberto."""
    print("\n--- Comandas em Aberto ---")
    if comandas:
        for i, comanda in enumerate(comandas):
            print(f"\n--- Comanda {i+1} ---")
            total = 0.0
            tabela = [[item["produto"].nome, item["quantidade"], f"R$ {item['produto'].preco * item['quantidade']:.2f}"] for item in comanda["itens"]]
            cabecalhos = ["Item", "Quantidade", "Subtotal"]
            print(tabulate(tabela, headers=cabecalhos, tablefmt="grid", numalign="right", stralign="left"))
            for item in comanda["itens"]:
                total += item['produto'].preco * item['quantidade']
            print(f"\nTotal: R$ {total:.2f}")
    else:
        print("Nenhuma comanda em aberto.")

def fazer_pedido(repo: ProdutoRepo):
    """Permite ao usuário fazer um pedido, adicionando itens à comanda."""
    print("\n--- Fazer Pedido ---")
    exibir_cardapio(repo)
    comanda = {"itens": []}
    total = 0.0
    while True:
        try:
            item_id = int(input("Digite o ID do item desejado (ou 0 para finalizar): "))
            if item_id == 0:
                break
            produto = repo.obter(item_id)
            if produto:
                quantidade = int(input(f"Digite a quantidade de '{produto.nome}': "))
                if quantidade > 0:
                    comanda["itens"].append({"produto": produto, "quantidade": quantidade})
                    total += produto.preco * quantidade
                else:
                    print("Quantidade inválida.")
            else:
                print("Item não encontrado no cardápio.")
        except ValueError:
            print("Entrada inválida. Digite um ID válido (inteiro).")

    if comanda["itens"]:
        print("\n--- Comanda ---")
        tabela = [[item["produto"].nome, item["quantidade"], f"R$ {item['produto'].preco * item['quantidade']:.2f}"] for item in comanda["itens"]]
        cabecalhos = ["Item", "Quantidade", "Subtotal"]
        print(tabulate(tabela, headers=cabecalhos, tablefmt="grid", numalign="right", stralign="left"))
        print(f"\nTotal: R$ {total:.2f}")
        comandas.append(comanda)
    else:
        print("Nenhum item adicionado à comanda.")


def exibir_menu():
    """Exibe o menu principal."""
    print("\n--- Sistema de Caixa ---")
    print("1) Ver Cardápio")
    print("2) Listar Comandas")
    print("3) Fazer Pedido")
    print("4) Sair")
    print("-----------------------")

def main():
    """Função principal."""
    repo = ProdutoRepo()

    # Deleta todos os produtos do cardápio
    repo.excluir_todos()

    # Adicionando os itens do cardápio
    hamburguers = [
        {"nome": "Clássico", "preco": 22.00, "ingredientes": "Pão brioche, carne 180g, queijo cheddar, picles, molho especial"},
        {"nome": "Bacon Deluxe", "preco": 28.00, "ingredientes": "Pão brioche, carne 180g, queijo cheddar, bacon, cebola caramelizada, molho barbecue"},
        {"nome": "Vegetariano", "preco": 25.00, "ingredientes": "Pão integral, hambúrguer de grão de bico, queijo muçarela, tomate seco, rúcula, maionese vegana"},
        {"nome": "Frango Crocante", "preco": 24.00, "ingredientes": "Pão brioche, frango crocante, queijo cheddar, alface americana, tomate, maionese"},
        {"nome": "Costela BBQ", "preco": 32.00, "ingredientes": "Pão australiano, carne de costela desfiada, queijo cheddar, cebola crispy, molho barbecue"},
        {"nome": "Burger do Chef", "preco": 35.00, "ingredientes": "Pão brioche, blend de carnes nobres, queijo gruyère, cogumelos salteados, aioli de alho negro"},
        {"nome": "Supremo", "preco": 40.00, "ingredientes": "Pão brioche, 2 carnes 180g, queijo cheddar, bacon, ovo, alface, tomate, molho especial"},
        {"nome": "Kids", "preco": 15.00, "ingredientes": "Pão brioche, carne 100g, queijo cheddar"}
    ]

    bebidas = [
        {"nome": "Suco de Laranja", "preco": 8.00},
        {"nome": "Suco de Morango", "preco": 9.00},
        {"nome": "Coca-Cola", "preco": 6.00},
        {"nome": "Guaraná Antarctica", "preco": 5.50}
    ]

    for hamburguer in hamburguers:
        try:
            novo_produto = Produto(nome=hamburguer["nome"], preco=hamburguer["preco"], estoque=100)
            repo.adicionar(novo_produto)
        except ValidationError as e:
            print(f"Erro ao cadastrar hamburguer {hamburguer['nome']}: {e}")

    for bebida in bebidas:
        try:
            novo_produto = Produto(nome=bebida["nome"], preco=bebida["preco"], estoque=50)
            repo.adicionar(novo_produto)
        except ValidationError as e:
            print(f"Erro ao cadastrar bebida {bebida['nome']}: {e}")


    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_cardapio(repo)
        elif opcao == "2":
            listar_comandas()
        elif opcao == "3":
            fazer_pedido(repo)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
