"""Interface de linha de comando para o Estoque Fácil."""

import sys

from src.estoque import (
    adicionar_produto,
    atualizar_quantidade,
    carregar_estoque,
    listar_produtos,
    produtos_com_estoque_baixo,
    remover_produto,
    salvar_estoque,
    valor_total_estoque,
)

LINHA = "─" * 55


def cabecalho():
    print(f"\n{'═' * 55}")
    print("             ESTOQUE FÁCIL  v1.0.0")
    print("    Controle de estoque para microempreendedores")
    print(f"{'═' * 55}\n")


def menu():
    print(LINHA)
    print("  [1] Adicionar produto")
    print("  [2] Listar produtos")
    print("  [3] Atualizar quantidade")
    print("  [4] Remover produto")
    print("  [5] Produtos com estoque baixo")
    print("  [6] Valor total do estoque")
    print("  [0] Sair")
    print(LINHA)


def exibir_produto(p: dict):
    print(
        f"  ID:{p['id']:>3}  {p['nome']:<22} "
        f"Qtd:{p['quantidade']:>5}  "
        f"R${p['preco']:>8.2f}  [{p['categoria']}]"
    )


def cmd_adicionar(produtos):
    print(f"\n{LINHA}")
    print("  ADICIONAR PRODUTO")
    nome = input("  Nome do produto : ").strip()
    categoria = input("  Categoria       : ").strip() or "Geral"
    try:
        quantidade = int(input("  Quantidade      : "))
        preco = float(input("  Preço (R$)      : "))
        p = adicionar_produto(produtos, nome, quantidade, preco, categoria)
        print(f"\n  ✅ Produto '{p['nome']}' adicionado com ID {p['id']}.")
    except ValueError as e:
        print(f"\n  ❌ Erro: {e}")


def cmd_listar(produtos):
    print(f"\n{LINHA}")
    filtro = input("  Filtrar por categoria (Enter para todos): ").strip() or None
    itens = listar_produtos(produtos, filtro)
    if not itens:
        print("  Nenhum produto encontrado.")
        return
    print(f"\n  {'ID':<5} {'Nome':<22} {'Qtd':>5}  {'Preço':>10}  Categoria")
    print(f"  {'-'*53}")
    for p in itens:
        exibir_produto(p)
    print(f"\n  Total: {len(itens)} produto(s)")


def cmd_atualizar(produtos):
    print(f"\n{LINHA}")
    try:
        pid = int(input("  ID do produto   : "))
        nova_qtd = int(input("  Nova quantidade : "))
        p = atualizar_quantidade(produtos, pid, nova_qtd)
        print(f"\n  ✅ '{p['nome']}' atualizado para {nova_qtd} unidades.")
    except (ValueError, KeyError) as e:
        print(f"\n  ❌ Erro: {e}")


def cmd_remover(produtos):
    print(f"\n{LINHA}")
    try:
        pid = int(input("  ID do produto a remover: "))
        p = remover_produto(produtos, pid)
        print(f"\n  ✅ Produto '{p['nome']}' removido.")
    except (ValueError, KeyError) as e:
        print(f"\n  ❌ Erro: {e}")


def cmd_estoque_baixo(produtos):
    print(f"\n{LINHA}")
    try:
        limite = int(input("  Limite mínimo (padrão 5): ") or "5")
        itens = produtos_com_estoque_baixo(produtos, limite)
        if not itens:
            print("  ✅ Nenhum produto com estoque baixo.")
        else:
            print(f"\n  ⚠️  {len(itens)} produto(s) com estoque ≤ {limite}:\n")
            for p in itens:
                exibir_produto(p)
    except ValueError as e:
        print(f"\n  ❌ Erro: {e}")


def cmd_valor_total(produtos):
    total = valor_total_estoque(produtos)
    print(f"\n  Valor total do estoque: R$ {total:.2f}")


def main():
    cabecalho()
    produtos = carregar_estoque()

    while True:
        menu()
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            cmd_adicionar(produtos)
            salvar_estoque(produtos)
        elif opcao == "2":
            cmd_listar(produtos)
        elif opcao == "3":
            cmd_atualizar(produtos)
            salvar_estoque(produtos)
        elif opcao == "4":
            cmd_remover(produtos)
            salvar_estoque(produtos)
        elif opcao == "5":
            cmd_estoque_baixo(produtos)
        elif opcao == "6":
            cmd_valor_total(produtos)
        elif opcao == "0":
            print("\n  Até logo! \n")
            sys.exit(0)
        else:
            print("\n  ❌ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
