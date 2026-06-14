from .database import get_client

def listar_produtos():
    sb = get_client()
    response = sb.table("produtos").select("*").execute()
    return response.data

def buscar_produto(produto_id):
    sb = get_client()
    response = sb.table("produtos").select("*").eq("id", produto_id).execute()
    return response.data[0] if response.data else None

def criar_produto(nome, quantidade, preco, estoque_minimo=5):
    sb = get_client()
    response = sb.table("produtos").insert({
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco,
        "estoque_minimo": estoque_minimo
    }).execute()
    return response.data[0]

def atualizar_quantidade(produto_id, nova_quantidade):
    sb = get_client()
    response = sb.table("produtos").update({
        "quantidade": nova_quantidade
    }).eq("id", produto_id).execute()
    return response.data[0]

def deletar_produto(produto_id):
    sb = get_client()
    sb.table("produtos").delete().eq("id", produto_id).execute()
    return True

def produtos_estoque_baixo():
    sb = get_client()
    # retorna produtos onde quantidade <= estoque_minimo
    response = sb.table("produtos").select("*").execute()
    return [p for p in response.data if p["quantidade"] <= p["estoque_minimo"]]

def valor_total_estoque():
    produtos = listar_produtos()
    return sum(p["preco"] * p["quantidade"] for p in produtos)
