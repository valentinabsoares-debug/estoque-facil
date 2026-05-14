import requests

BASE_URL = "https://pokeapi.co/api/v2"

def buscar_pokemon(nome_ou_id: str) -> dict:
    """Busca dados de um Pokémon pelo nome ou ID."""
    nome = str(nome_ou_id).lower().strip()
    url = f"{BASE_URL}/pokemon/{nome}"
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        raise ValueError(f"Pokémon '{nome_ou_id}' não encontrado.")

    response.raise_for_status()
    dados = response.json()

    return {
        "nome": dados["name"].capitalize(),
        "id": dados["id"],
        "altura": dados["height"] / 10,   # decímetros → metros
        "peso": dados["weight"] / 10,     # hectogramas → kg
        "tipos": [t["type"]["name"] for t in dados["types"]],
        "habilidades": [h["ability"]["name"] for h in dados["abilities"]],
        "hp": dados["stats"][0]["base_stat"],
        "ataque": dados["stats"][1]["base_stat"],
        "defesa": dados["stats"][2]["base_stat"],
    }
