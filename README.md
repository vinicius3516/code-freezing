# Code Freezing

**Validação de congelamento de código em pipelines CI/CD**

O **Code Freezing** é um script em **Python** desenvolvido no contexto do curso [**Python para DevOps**](https://www.udemy.com/course/python-para-devops/?couponCode=KEEPLEARNINGBR), com o objetivo de **controlar períodos de congelamento de código** (code freeze) em pipelines de CI/CD.

Essa prática é comum em empresas que evitam deploys em períodos críticos, como **Black Friday, finais de ano ou eventos estratégicos**.

O script garante que **builds e deploys só avancem caso:**

- O usuário executor esteja autorizado no arquivo `config.yaml`, **OU**
- A execução não esteja dentro de um intervalo de datas configurado como congelamento.

---

> ## Funcionalidades

- Bloqueia execução de builds durante períodos de **congelamento configurados**.
- Permite exceções de usuários autorizados no arquivo `config.yaml`.
- Fácil integração com pipelines **GitHub Actions** (ou outras ferramentas CI/CD).
- Flexível: configuração simples via YAML.

---

> ## Estrutura do Projeto

```
code-freezing/
├── code-freezing.py      # Script principal
├── requirements.txt      # Dependências do projeto
├── config.yaml           # Configuração de usuários e períodos de freeze
└── README.md             # Documentação
```

---

> ## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/vinicius3516/code-freezing.git
cd code-freezing
pip install -r requirements.txt
```

---

> ## Uso

### 1. Configuração

No arquivo `config.yaml`, configure os períodos de congelamento e usuários autorizados.

Exemplo:

```yaml
bypass_group:
  - vinicius3516

freezing_dates:
  End of the year:
    from: 2025-12-24
    to: 2026-01-10

  Carnival:
    from: 2026-03-18
    to: 2026-02-22
```

### 2. Execução

Rodar o script diretamente:

```bash
python3 code-freezing.py
```

Em pipelines (exemplo com **GitHub Actions**):

```yaml
jobs:
  code-freeze-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout current repo
        uses: actions/checkout@v4

      - name: Checkout code-freezing
        uses: actions/checkout@v4
        with:
          repository: vinicius3516/code-freezing
          path: code-freezing

      - name: Python Setup
        uses: actions/setup-python@v5
        with:
          python-version: '3.10.12'

      - name: Install dependencies
        working-directory: code-freezing
        run: |
          pip install -r requirements.txt

      - name: Run code freeze check
        working-directory: code-freezing
        env:
          GITHUB_ACTOR: ${{ github.actor }}
        run: |
          python3 code-freezing.py
```

Se o período estiver congelado e o usuário **não estiver autorizado**, o pipeline é bloqueado.

---

> ## Exemplo de Fluxo

1. PR aberto → GitHub Actions inicia.
2. **Job `code-freeze-check`** executa o script.
3. Se dentro do período de congelamento → bloqueia.
4. Caso contrário → segue para **build/deploy**.
