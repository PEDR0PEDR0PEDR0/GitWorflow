# Guia de Contribuição (GitHub Flow)

Este repositório adota o **GitHub Flow** como modelo oficial de desenvolvimento colaborativo, combinado com automações completas de CI/CD, governança e segurança via **GitHub Actions**.

## Fluxo de Trabalho (GitHub Flow)

1. **Mantenha a `main` sempre implantável:** nenhum commit é enviado diretamente para `main` (protegida por Ruleset).
2. **Crie uma branch descritiva a partir da `main`:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/nova-operacao
   ```
   Prefixos recomendados: `feat/`, `fix/`, `docs/`, `ci/`, `refactor/`, `test/`, `chore/`, `hotfix/`.
3. **Desenvolva com commits claros e atômicos** seguindo [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat(operacoes): adiciona cálculo de fatorial`
   - `fix(operacoes): corrige fórmula da função somar`
   - `ci(pages): adiciona estágio de staging antes da produção`
   - `docs(tcc): detalha arquitetura de reusable workflows`
4. **Valide localmente antes de abrir o Pull Request:**
   ```bash
   python -m venv .venv
   # Windows (PowerShell): .\.venv\Scripts\Activate.ps1
   # Linux/macOS:          source .venv/bin/activate
   pip install -e ".[dev,build]"

   ruff check .
   ruff format --check .
   mypy calculadora tests scripts
   python scripts/validate_workflows.py
   python -m pytest -v --cov=calculadora --cov-fail-under=90
   bandit -r calculadora scripts -ll
   ```
5. **Abra o Pull Request para `main`:**
   - Use um título no padrão **Conventional Commits** (validado automaticamente por `pr-governance.yml`).
   - Preencha o template de Pull Request vinculando a issue relacionada (`Closes #<id>`).
   - Aguarde a conclusão de todos os checks obrigatórios (`testes`, governança e segurança) e a revisão de código (`CODEOWNERS`).
6. **Merge e Entrega Contínua:**
   - Após aprovação e checks verdes, faça o merge (preferencialmente *Squash and merge* para histórico linear).
   - O merge dispara automaticamente o deploy no GitHub Pages (`cd-pages.yml`).
   - Apague a branch de feature após o merge.

## Padrões de Código

- Python **3.11+** com anotações de tipo completas (`mypy --strict`).
- Formatação e lint padronizados via **Ruff** (`line-length = 100`).
- Cobertura mínima obrigatória de **90%** no pacote `calculadora`.
- Workflows em `.github/workflows/` devem declarar `permissions` mínimas e `timeout-minutes` em todos os jobs.
