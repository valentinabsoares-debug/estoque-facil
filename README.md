~ Estoque Fácil

[![CI](https://github.com/valentinabsoares-debug/estoque-facil/actions/workflows/ci.yml/badge.svg)](https://github.com/valentinabsoares-debug/estoque-facil/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Versão](https://img.shields.io/badge/versão-1.0.0-green)
![Licença](https://img.shields.io/badge/licença-MIT-lightgrey)

---

O Problema

Microempreendedores — como vendedores de roupas, artesãos, revendedores e donos de pequenos comércios — frequentemente perdem o controle do próprio estoque por falta de uma ferramenta simples e gratuita. Planilhas são complexas e sistemas pagos são caros. O resultado são produtos em falta, compras desnecessárias e prejuízo financeiro.

A Solução

**Estoque Fácil** é um aplicativo de linha de comando (CLI) gratuito, leve e sem necessidade de internet, que permite cadastrar produtos, controlar quantidades, receber alertas de estoque baixo e visualizar o valor total do estoque — tudo em segundos, diretamente no terminal.

---

Público-alvo

- Vendedores autônomos e revendedores
- Artesãos e produtores independentes
- Donos de pequenos comércios e microempreendedores individuais (MEI)

---

Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Adicionar produto | Cadastra nome, quantidade, preço e categoria |
| Listar produtos | Exibe todos os produtos ou filtra por categoria |
| Atualizar quantidade | Edita a quantidade de um produto pelo ID |
| Remover produto | Remove um produto do estoque |
| Estoque baixo | Alerta produtos abaixo de um limite configurável |
| Valor total | Calcula o valor total do estoque |

Os dados são salvos automaticamente em um arquivo `estoque.json` na pasta do projeto.

---

Tecnologias

- **Python 3.11+** — linguagem principal
- **Pytest** — testes automatizados
- **Ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)

Sem dependências externas para a aplicação em si — apenas a biblioteca padrão do Python.

---

Instalação

**Pré-requisito:** Python 3.11 ou superior instalado.

```bash
# 1. Clonar o repositório
git clone https://github.com/valentinabsoares-debug/estoque-facil.git
cd estoque-facil

# 2. Criar um ambiente virtual (Opcional)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Instalar as dependências de desenvolvimento
pip install -r requirements.txt
```

---

Execução

```bash
python main.py
```

Você verá o menu interativo:

```
═══════════════════════════════════════════════════════
             ESTOQUE FÁCIL  v1.0.0
    Controle de estoque para microempreendedores
═══════════════════════════════════════════════════════

───────────────────────────────────────────────────────
  [1] Adicionar produto
  [2] Listar produtos
  [3] Atualizar quantidade
  [4] Remover produto
  [5] Produtos com estoque baixo
  [6] Valor total do estoque
  [0] Sair
───────────────────────────────────────────────────────
  Escolha uma opção:
```

---

Rodando os Testes

```bash
pytest -v
```

Saída esperada: **21 testes passando**, cobrindo cenários de sucesso, entradas inválidas e casos limite.

```
tests/test_estoque.py::TestAdicionarProduto::test_adiciona_produto_valido PASSED
tests/test_estoque.py::TestAdicionarProduto::test_nome_vazio_levanta_erro PASSED
tests/test_estoque.py::TestAdicionarProduto::test_quantidade_negativa_levanta_erro PASSED
...
21 passed in 0.XX s
```

---

Rodando o Lint

```bash
ruff check .
```

Nenhum problema deve ser reportado. Para corrigir automaticamente o que for possível:

```bash
ruff check . --fix
```

---

Estrutura do Projeto

```
estoque-facil/
├── src/
│   ├── __init__.py
│   └── estoque.py          # Lógica de negócio
├── tests/
│   ├── __init__.py
│   └── test_estoque.py     # Testes automatizados
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline GitHub Actions
├── main.py                 # Interface CLI
├── pyproject.toml          # Configuração e versão do projeto
├── requirements.txt        # Dependências de desenvolvimento
├── CHANGELOG.md
├── LICENSE
├── .gitignore
└── README.md
```

---

Pipeline CI (GitHub Actions)

A cada `push` ou `pull request` para a branch `main`, a pipeline executa automaticamente:

1. Checkout do código
2. Configuração do Python 3.11
3. Instalação das dependências
4. **Linting com Ruff**
5. **Testes com Pytest**

---

Versão

**1.0.0** — Consulte o [CHANGELOG.md](CHANGELOG.md) para o histórico de mudanças.

---

Autor

**Valentina B. Soares**
- GitHub: [@valentinabsoares-debug](https://github.com/valentinabsoares-debug)

---

Repositório

[https://github.com/valentinabsoares-debug/estoque-facil](https://github.com/valentinabsoares-debug/estoque-facil)

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.
