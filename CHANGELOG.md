# Changelog

Todas as alterações relevantes deste projeto são documentadas neste arquivo.
O formato baseia-se em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

## [1.0.0] - 2026-11-24

### Adicionado
- Pacote Python estruturado `calculadora` (`pyproject.toml`, tipagem estrita `py.typed`, operações matemáticas completas, módulo de estatística descritiva, exceções de domínio e CLI `calculadora`).
- Suíte de testes abrangente (`unit`, `cli`, `pages`) com verificação mínima de 90% de cobertura.
- Composite Action local `.github/actions/setup-python-env` para reutilização de setup e cache `pip`.
- Reusable Workflow `.github/workflows/reusable-python-checks.yml` com inputs, outputs, artefatos e Step Summary.
- Pipeline completo de CI (`.github/workflows/ci.yml`) com Ruff, Mypy, validação de `.github/`, matriz OS × Python, empacotamento wheel/sdist e gate obrigatório `testes`.
- Governança de Pull Requests (`.github/workflows/pr-governance.yml`) com validação de Conventional Commits, padrão de branch, métrica de tamanho e auto-labeler (`.github/labeler.yml`).
- Pipeline de Segurança DevSecOps (`.github/workflows/security.yml`) com CodeQL, Bandit, `pip-audit` e Dependency Review.
- Entrega Contínua no GitHub Pages (`.github/workflows/cd-pages.yml`) com GitHub Environments (`staging` → `github-pages`) e gerador estático `scripts/build_pages.py`.
- Pipeline de Release automatizado (`.github/workflows/release.yml`) com SemVer, `SHA256SUMS.txt`, Build Provenance Attestation e notas categorizadas (`.github/release.yml`).
- Workflow de manutenção agendada (`.github/workflows/maintenance.yml`) com verificação semanal de saúde e `actions/stale`.
- Arquivos de governança e comunidade: `dependabot.yml`, `CODEOWNERS`, `PULL_REQUEST_TEMPLATE.md`, Issue Forms YAML, `.github/rulesets/main-protection.json`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` e `LICENSE`.
- Documentação técnica completa para o TCC em `docs/`.

### Corrigido
- Corrigida a operação `somar(a, b)` de `a - b` para `a + b`.
