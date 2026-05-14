from pokeapi import buscar_pokemon

def exibir_pokemon(dados: dict):
    linha = "-" * 35
    print(f"\n{linha}")
    print(f"  #{dados['id']} — {dados['nome']}")
    print(linha)
    print(f"  Tipos      : {', '.join(dados['tipos'])}")
    print(f"  Altura     : {dados['altura']} m")
    print(f"  Peso       : {dados['peso']} kg")
    print(f"  HP         : {dados['hp']}")
    print(f"  Ataque     : {dados['ataque']}")
    print(f"  Defesa     : {dados['defesa']}")
    print(f"  Habilidades: {', '.join(dados['habilidades'])}")
    print(f"{linha}\n")

def main():
    print("=== Pokédex CLI ===")
    while True:
        entrada = input("Nome ou número do Pokémon (ou 'sair'): ").strip()
        if entrada.lower() == "sair":
            print("Até mais!")
            break
        try:
            dados = buscar_pokemon(entrada)
            exibir_pokemon(dados)
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Falha na conexão: {e}")

if __name__ == "__main__":
    main()
