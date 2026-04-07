"""Módulo principal de controle de estoque."""

import json
import os
from datetime import datetime


ARQUIVO_ESTOQUE = "estoque.json"


def carregar_estoque(caminho: str = ARQUIVO_ESTOQUE) -> list[dict]:
    """Carrega os produtos do arquivo JSON."""
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_estoque(produtos: list[dict], caminho: str = ARQUIVO_ESTOQUE) -> None:
    """Salva os produtos no arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)


def adicionar_produto(
    produtos: list[dict],
    nome: str,
    quantidade: int,
    preco: float,
    categoria: str = "Geral",
) -> dict:
    """Adiciona um novo produto ao estoque."""
    if not nome or not nome.strip():
        raise ValueError("O nome do produto não pode ser vazio.")
    if quantidade < 0:
        raise ValueError("A quantidade não pode ser negativa.")
    if preco < 0:
        raise ValueError("O preço não pode ser negativo.")

    novo_id = max((p["id"] for p in produtos), default=0) + 1
    produto = {
        "id": novo_id,
        "nome": nome.strip(),
        "quantidade": quantidade,
        "preco": round(preco, 2),
        "categoria": categoria.strip() or "Geral",
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    produtos.append(produto)
    return produto


def listar_produtos(produtos: list[dict], categoria: str | None = None) -> list[dict]:
    """Retorna todos os produtos, com filtro opcional por categoria."""
    if categoria:
        return [p for p in produtos if p["categoria"].lower() == categoria.lower()]
    return list(produtos)


def buscar_produto(produtos: list[dict], produto_id: int) -> dict | None:
    """Busca um produto pelo ID."""
    for p in produtos:
        if p["id"] == produto_id:
            return p
    return None


def atualizar_quantidade(
    produtos: list[dict], produto_id: int, nova_quantidade: int
) -> dict:
    """Atualiza a quantidade de um produto."""
    if nova_quantidade < 0:
        raise ValueError("A quantidade não pode ser negativa.")
    produto = buscar_produto(produtos, produto_id)
    if produto is None:
        raise KeyError(f"Produto com ID {produto_id} não encontrado.")
    produto["quantidade"] = nova_quantidade
    return produto


def remover_produto(produtos: list[dict], produto_id: int) -> dict:
    """Remove um produto do estoque pelo ID."""
    for i, p in enumerate(produtos):
        if p["id"] == produto_id:
            return produtos.pop(i)
    raise KeyError(f"Produto com ID {produto_id} não encontrado.")


def produtos_com_estoque_baixo(produtos: list[dict], limite: int = 5) -> list[dict]:
    """Retorna produtos com quantidade abaixo ou igual ao limite."""
    return [p for p in produtos if p["quantidade"] <= limite]


def valor_total_estoque(produtos: list[dict]) -> float:
    """Calcula o valor total do estoque (quantidade × preço)."""
    return round(sum(p["quantidade"] * p["preco"] for p in produtos), 2)
