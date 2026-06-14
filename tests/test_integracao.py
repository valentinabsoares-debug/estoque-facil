import responses
import pytest
from pokeapi import buscar_pokemon

MOCK_PIKACHU = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": [{"type": {"name": "electric"}}],
    "abilities": [
        {"ability": {"name": "static"}},
        {"ability": {"name": "lightning-rod"}}
    ],
    "stats": [
        {"base_stat": 35},  # hp
        {"base_stat": 55},  # ataque
        {"base_stat": 40},  # defesa
    ]
}

@responses.activate
def test_buscar_pikachu_retorna_dados_corretos():
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/pikachu",
        json=MOCK_PIKACHU,
        status=200
    )
    resultado = buscar_pokemon("pikachu")

    assert resultado["nome"] == "Pikachu"
    assert resultado["id"] == 25
    assert "electric" in resultado["tipos"]
    assert resultado["hp"] == 35

@responses.activate
def test_pokemon_inexistente_levanta_value_error():
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/fakemon",
        status=404
    )
    with pytest.raises(ValueError, match="fakemon"):
        buscar_pokemon("fakemon")

@responses.activate
def test_busca_por_numero():
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/25",
        json=MOCK_PIKACHU,
        status=200
    )
    resultado = buscar_pokemon(25)
    assert resultado["nome"] == "Pikachu"
