# Roteiro de Demonstração Prática para o TCC

Este roteiro organiza **5 demonstrações ao vivo** (ou gravadas como evidência) que comprovam na prática todos os pilares do GitHub Workflow implementados no repositório.

---

## Cenário 1 — Proteção da `main` e Bloqueio por Falha na CI

**Objetivo:** provar que código defeituoso ou fora do padrão não entra na branch principal.

1. Crie uma branch de demonstração a partir da `main`:
   ```bash
   git checkout main && git pull
   git checkout -b fix/demo-falha-ci
   ```
2. Introduza intencionalmente um erro em `calculadora/operacoes.py` (por exemplo, `return a - b` em `somar`) ou abra um PR com título fora de Conventional Commits (ex.: `ajustando soma`).
3. Faça `push` e abra o Pull Request para `main`:
   - **O que mostrar à banca:**
     - O workflow `PR Governance` falha imediatamente se o título violar Conventional Commits e aplica automaticamente as labels (`python`) via `.github/labeler.yml`.
     - O workflow `CI` executa em paralelo `qualidade`, a matriz 5× (`ubuntu`/`windows`/`macos` × Python `3.11`/`3.12`/`3.13`) e `empacotamento`.
     - O gate job `testes` falha e o **Ruleset da `main` bloqueia o botão de Merge**.

---

## Cenário 2 — Correção, Checks Verdes e Step Summary

**Objetivo:** mostrar feedback rápido, reutilização de workflows e desbloqueio automático do merge.

1. Corrija o código (`return a + b`) e ajuste o título do PR para `fix(operacoes): corrige soma na demonstração`.
2. Faça `git push`:
   - **O que mostrar à banca:**
     - O recurso `concurrency` cancela automaticamente a execução antiga do PR se outra estiver em andamento.
     - Todos os checks ficam verdes (`qualidade`, matriz multi-SO, cobertura ≥ 90%, build do wheel + smoke test da CLI, `Bandit`, `CodeQL`, `pip-audit`, `Dependency Review` e o gate `testes`).
     - Abra a aba **Summary** da execução da CI para exibir a tabela consolidada gerada em `$GITHUB_STEP_SUMMARY` e os artefatos baixáveis (`relatorios-ci-*` e `pacote-dist`).

---

## Cenário 3 — Entrega Contínua (CD) com GitHub Environments e GitHub Pages

**Objetivo:** demonstrar promoção entre ambientes (`staging` → `github-pages`) e publicação automática pós-merge.

1. Faça **Squash and merge** do PR aprovado na `main`.
2. Abra a aba **Actions → CD GitHub Pages**:
   - **O que mostrar à banca:**
     - O job `build-portal` roda a suíte de testes, gera o relatório HTML de cobertura e constrói `_site/` via `scripts/build_pages.py`.
     - O job `validar-staging` entra no ambiente `staging` *(se você ativou Required Reviewers em `staging`, aprove ao vivo na tela da banca!)*.
     - O job `deploy-production` publica via OIDC no ambiente `github-pages` e exibe a URL pública do portal.
3. Acesse o portal publicado e clique em **Abrir Relatório HTML de Cobertura**, destacando o commit SHA, versão e percentual de cobertura atualizados automaticamente.

---

## Cenário 4 — Release Automatizado (SemVer + Build Provenance Attestation)

**Objetivo:** provar empacotamento reprodutível, checksums e rastreabilidade criptográfica da cadeia de suprimentos.

1. Primeiro, mostre o modo **dry-run** via **Actions → Release → Run workflow** (`tag: v1.0.0`, `publicar_release: false`).
2. Em seguida, crie e envie a tag oficial:
   ```bash
   git checkout main && git pull
   git tag -a v1.0.0 -m "Release v1.0.0 — Implementação completa de GitHub Workflow"
   git push origin v1.0.0
   ```
3. **O que mostrar à banca:**
   - Validação automática de SemVer e sincronia entre a tag `v1.0.0` e `calculadora.__version__`.
   - Nova página em **Releases** com notas categorizadas automaticamente por `.github/release.yml` e anexos (`.whl`, `.tar.gz`, `SHA256SUMS.txt`).
   - Registro criptográfico em **Actions → Attestations** comprovando a origem do artefato (`actions/attest-build-provenance`).

---

## Cenário 5 — Segurança Contínua e Automação Preventiva

**Objetivo:** demonstrar operação contínua mesmo sem novos commits.

1. Mostre a aba **Security**:
   - **Code scanning** com resultados do CodeQL.
   - **Dependabot** monitorando tanto `pip` quanto `github-actions` (`.github/dependabot.yml`).
2. Dispare manualmente o workflow **Maintenance** (`workflow_dispatch`) para demonstrar o relatório periódico de saúde e a política de `actions/stale`.
3. Mostre a página **Insights → Community Standards** atingindo 100% de conformidade (`README`, `CODE_OF_CONDUCT`, `CONTRIBUTING`, `LICENSE`, `SECURITY`, Issue Forms e PR Template).
