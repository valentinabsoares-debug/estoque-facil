"""Testes automatizados para o módulo de estoque."""

import pytest

from src.estoque import (
    adicionar_produto,
    atualizar_quantidade,
    listar_produtos,
    produtos_com_estoque_baixo,
    remover_produto,
    valor_total_estoque,
)


# ── Fixtures ──────────────────────────────────────────────

@pytest.fixture
def estoque_vazio():
    return []


@pytest.fixture
def estoque_exemplo():
    produtos = []
    adicionar_produto(produtos, "Camiseta", 50, 39.90, "Roupas")
    adicionar_produto(produtos, "Calça Jeans", 20, 89.90, "Roupas")
    adicionar_produto(produtos, "Boné", 3, 25.00, "Acessórios")
    return produtos


# ── Testes: adicionar produto ──────────────────────────────

class TestAdicionarProduto:
    def test_adiciona_produto_valido(self, estoque_vazio):
        p = adicionar_produto(estoque_vazio, "Mochila", 10, 120.00)
        assert p["nome"] == "Mochila"
        assert p["quantidade"] == 10
        assert p["preco"] == 120.00
        assert len(estoque_vazio) == 1

    def test_ids_sequenciais(self, estoque_vazio):
        adicionar_produto(estoque_vazio, "A", 1, 1.0)
        adicionar_produto(estoque_vazio, "B", 2, 2.0)
        assert estoque_vazio[0]["id"] == 1
        assert estoque_vazio[1]["id"] == 2

    def test_categoria_padrao_geral(self, estoque_vazio):
        p = adicionar_produto(estoque_vazio, "Produto X", 5, 10.0)
        assert p["categoria"] == "Geral"

    def test_nome_vazio_levanta_erro(self, estoque_vazio):
        with pytest.raises(ValueError, match="nome"):
            adicionar_produto(estoque_vazio, "", 5, 10.0)

    def test_quantidade_negativa_levanta_erro(self, estoque_vazio):
        with pytest.raises(ValueError, match="quantidade"):
            adicionar_produto(estoque_vazio, "Produto", -1, 10.0)

    def test_preco_negativo_levanta_erro(self, estoque_vazio):
        with pytest.raises(ValueError, match="preço"):
            adicionar_produto(estoque_vazio, "Produto", 5, -10.0)

    def test_quantidade_zero_permitida(self, estoque_vazio):
        p = adicionar_produto(estoque_vazio, "Produto", 0, 10.0)
        assert p["quantidade"] == 0


# ── Testes: listar produtos ────────────────────────────────

class TestListarProdutos:
    def test_lista_todos(self, estoque_exemplo):
        itens = listar_produtos(estoque_exemplo)
        assert len(itens) == 3

    def test_filtra_por_categoria(self, estoque_exemplo):
        itens = listar_produtos(estoque_exemplo, "Roupas")
        assert len(itens) == 2
        assert all(p["categoria"] == "Roupas" for p in itens)

    def test_filtro_case_insensitive(self, estoque_exemplo):
        itens = listar_produtos(estoque_exemplo, "roupas")
        assert len(itens) == 2

    def test_categoria_inexistente_retorna_vazio(self, estoque_exemplo):
        itens = listar_produtos(estoque_exemplo, "Eletrônicos")
        assert itens == []

    def test_estoque_vazio_retorna_lista_vazia(self, estoque_vazio):
        assert listar_produtos(estoque_vazio) == []


# ── Testes: atualizar quantidade ───────────────────────────

class TestAtualizarQuantidade:
    def test_atualiza_com_sucesso(self, estoque_exemplo):
        pid = estoque_exemplo[0]["id"]
        p = atualizar_quantidade(estoque_exemplo, pid, 99)
        assert p["quantidade"] == 99

    def test_quantidade_zero_permitida(self, estoque_exemplo):
        pid = estoque_exemplo[0]["id"]
        p = atualizar_quantidade(estoque_exemplo, pid, 0)
        assert p["quantidade"] == 0

    def test_quantidade_negativa_levanta_erro(self, estoque_exemplo):
        pid = estoque_exemplo[0]["id"]
        with pytest.raises(ValueError):
            atualizar_quantidade(estoque_exemplo, pid, -5)

    def test_id_inexistente_levanta_erro(self, estoque_exemplo):
        with pytest.raises(KeyError):
            atualizar_quantidade(estoque_exemplo, 9999, 10)


# ── Testes: remover produto ────────────────────────────────

class TestRemoverProduto:
    def test_remove_com_sucesso(self, estoque_exemplo):
        pid = estoque_exemplo[0]["id"]
        removido = remover_produto(estoque_exemplo, pid)
        assert removido["id"] == pid
        assert len(estoque_exemplo) == 2

    def test_id_inexistente_levanta_erro(self, estoque_exemplo):
        with pytest.raises(KeyError):
            remover_produto(estoque_exemplo, 9999)

    def test_estoque_vazio_levanta_erro(self, estoque_vazio):
        with pytest.raises(KeyError):
            remover_produto(estoque_vazio, 1)


# ── Testes: estoque baixo ──────────────────────────────────

class TestEstoqueBaixo:
    def test_detecta_estoque_baixo(self, estoque_exemplo):
        # Boné tem 3 unidades
        baixos = produtos_com_estoque_baixo(estoque_exemplo, limite=5)
        assert any(p["nome"] == "Boné" for p in baixos)

    def test_nenhum_produto_baixo(self, estoque_exemplo):
        baixos = produtos_com_estoque_baixo(estoque_exemplo, limite=2)
        assert baixos == []

    def test_limite_exato_incluido(self, estoque_exemplo):
        # Boné tem exatamente 3 unidades — deve ser incluído no limite=3
        baixos = produtos_com_estoque_baixo(estoque_exemplo, limite=3)
        assert any(p["nome"] == "Boné" for p in baixos)


# ── Testes: valor total ────────────────────────────────────

class TestValorTotalEstoque:
    def test_calculo_correto(self, estoque_exemplo):
        # 50×39.90 + 20×89.90 + 3×25.00 = 1995 + 1798 + 75 = 3868
        total = valor_total_estoque(estoque_exemplo)
        assert total == pytest.approx(3868.00, rel=1e-2)

    def test_estoque_vazio_retorna_zero(self, estoque_vazio):
        assert valor_total_estoque(estoque_vazio) == 0.0

    def test_produto_sem_quantidade(self, estoque_vazio):
        adicionar_produto(estoque_vazio, "Sem estoque", 0, 100.0)
        assert valor_total_estoque(estoque_vazio) == 0.0
