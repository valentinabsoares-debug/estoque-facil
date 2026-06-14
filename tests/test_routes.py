import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Mock para não precisar do banco real nos testes
PRODUTO_FAKE = {
    "id": 1, "nome": "Arroz", "quantidade": 10,
    "preco": 5.99, "estoque_minimo": 5
}

def test_listar_produtos(client):
    with patch("app.routes.listar_produtos", return_value=[PRODUTO_FAKE]):
        response = client.get("/produtos")
        assert response.status_code == 200
        assert len(response.get_json()) == 1

def test_criar_produto(client):
    with patch("app.routes.criar_produto", return_value=PRODUTO_FAKE):
        response = client.post("/produtos", json={
            "nome": "Arroz", "quantidade": 10,
            "preco": 5.99, "estoque_minimo": 5
        })
        assert response.status_code == 201

def test_produto_nao_encontrado(client):
    with patch("app.routes.buscar_produto", return_value=None):
        response = client.get("/produtos/999")
        assert response.status_code == 404

def test_estoque_baixo(client):
    produto_baixo = {**PRODUTO_FAKE, "quantidade": 2}
    with patch("app.routes.produtos_estoque_baixo", return_value=[produto_baixo]):
        response = client.get("/alertas/estoque-baixo")
        assert response.status_code == 200

def test_valor_total(client):
    with patch("app.routes.valor_total_estoque", return_value=59.90):
        response = client.get("/relatorio/valor-total")
        assert response.status_code == 200
        assert response.get_json()["valor_total"] == 59.90
