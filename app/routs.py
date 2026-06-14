from flask import Blueprint, jsonify, request
from .models import (
    listar_produtos, buscar_produto, criar_produto,
    atualizar_quantidade, deletar_produto,
    produtos_estoque_baixo, valor_total_estoque
)

bp = Blueprint("produtos", __name__)

@bp.route("/produtos", methods=["GET"])
def get_produtos():
    return jsonify(listar_produtos())

@bp.route("/produtos/<int:produto_id>", methods=["GET"])
def get_produto(produto_id):
    produto = buscar_produto(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto)

@bp.route("/produtos", methods=["POST"])
def post_produto():
    dados = request.get_json()
    produto = criar_produto(
        nome=dados["nome"],
        quantidade=dados["quantidade"],
        preco=dados["preco"],
        estoque_minimo=dados.get("estoque_minimo", 5)
    )
    return jsonify(produto), 201

@bp.route("/produtos/<int:produto_id>/quantidade", methods=["PATCH"])
def patch_quantidade(produto_id):
    dados = request.get_json()
    produto = atualizar_quantidade(produto_id, dados["quantidade"])
    return jsonify(produto)

@bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def delete_produto(produto_id):
    deletar_produto(produto_id)
    return jsonify({"mensagem": "Produto removido"}), 200

@bp.route("/alertas/estoque-baixo", methods=["GET"])
def get_estoque_baixo():
    return jsonify(produtos_estoque_baixo())

@bp.route("/relatorio/valor-total", methods=["GET"])
def get_valor_total():
    return jsonify({"valor_total": valor_total_estoque()})
