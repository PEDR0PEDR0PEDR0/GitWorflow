# Guia de Configuração no GitHub (Rulesets, Environments, Pages e Segurança)

Parte da governança de um GitHub Workflow vive no código (`.github/`), e outra parte vive nas configurações da plataforma GitHub. Este guia garante a reprodutibilidade completa do ambiente para o TCC.

---

## 1. Habilitar GitHub Pages via GitHub Actions

1. Acesse **Settings → Pages** no repositório `PEDR0PEDR0PEDR0/GitWorflow`.
2. Em **Build and deployment → Source**, selecione **GitHub Actions** (não use *Deploy from a branch*).
3. Após o primeiro merge na `main`, o workflow `CD GitHub Pages` publicará automaticamente o portal em:
   `https://pedr0pedr0pedr0.github.io/GitWorflow/`

---

## 2. Configurar GitHub Environments (`staging`, `github-pages`, `release`)

Acesse **Settings → Environments** e configure os três ambientes usados pelos workflows de CD e Release:

1. **`staging`** (usado em `.github/workflows/cd-pages.yml`):
   - *(Opcional para demonstração de aprovação na banca)* Ative **Required reviewers** e adicione `@PEDR0PEDR0PEDR0` — assim, o deploy pausa entre o build e a publicação em produção aguardando aprovação manual!
   - Em **Deployment branches and tags**, restrinja para `Selected branches and tags` → branch `main`.
2. **`github-pages`** (criado automaticamente ao habilitar Pages com Actions):
   - Em **Deployment branches and tags**, mantenha apenas a branch `main`.
3. **`release`** (usado em `.github/workflows/release.yml`):
   - Ative **Required reviewers** (`@PEDR0PEDR0PEDR0`) se desejar aprovação explícita antes de publicar releases.
   - Em **Deployment branches and tags**, permita tags com padrão `v*.*.*` (e branch `main` para `workflow_dispatch`).

---

## 3. Aplicar ou Atualizar o Ruleset da Branch `main`

O arquivo declarativo `.github/rulesets/main-protection.json` contém todas as regras recomendadas para a `main`:

- Bloqueia exclusão da branch e `git push --force`.
- Exige histórico linear (recomendado usar **Squash and merge**).
- Exige Pull Request com revisão aprovada, dispensa aprovações obsoletas após novos pushes, exige revisão de `CODEOWNERS` e resolução de todas as conversas.
- Exige os status checks obrigatórios:
  - `testes` *(gate consolidado de todo o CI)*
  - `Validar Título, Branch e Tamanho do PR`
  - `Análise de Segurança Python (Bandit)`

### Opção A — Via Interface Web
1. Acesse **Settings → Rules → Rulesets → New ruleset → Import a ruleset**.
2. Importe o arquivo `.github/rulesets/main-protection.json` (ou atualize o ruleset existente na `main` com esses checks).
   > **Dica para repositório individual (1 mantenedor):** em contas pessoais onde o próprio autor abre e aprova seus PRs, o GitHub não permite auto-aprovação de PR. Nesse caso, ajuste temporariamente `required_approving_review_count` para `0` (mantendo PR obrigatório + checks obrigatórios) ou adicione seu usuário na *Bypass list* apenas para demonstrações solo, documentando esse ponto na apresentação do TCC.

### Opção B — Via GitHub CLI (`gh`)
```bash
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/PEDR0PEDR0PEDR0/GitWorflow/rulesets \
  --input .github/rulesets/main-protection.json
```

---

## 4. Ativar Recursos de Segurança (Code Security)

Acesse **Settings → Code security** (ou **Security & analysis**) e ative:

- **Dependency graph** *(necessário para `actions/dependency-review-action`)*
- **Dependabot alerts** e **Dependabot security updates**
- **Dependabot version updates** *(lê automaticamente `.github/dependabot.yml`)*
- **Code scanning** *(alimentado pelo job `codeql` em `.github/workflows/security.yml`)*
- **Secret scanning** e **Push protection** *(bloqueia acidentalmente commitar tokens/chaves)*
- **Private vulnerability reporting** *(alinha com `SECURITY.md`)*

---

## 5. Criar as Labels Usadas por `labeler.yml` e `release.yml`

Execute os comandos abaixo com o `gh` CLI autenticado (ou crie manualmente em **Issues → Labels**):

```bash
gh label create "ci/cd" --color "0E8A16" --description "Workflows, GitHub Actions e pipelines" --force
gh label create "governance" --color "5319E7" --description "Rulesets, templates, CODEOWNERS e políticas" --force
gh label create "security" --color "B60205" --description "CodeQL, Bandit, auditoria e segurança" --force
gh label create "python" --color "1D76DB" --description "Código do pacote Python e CLI" --force
gh label create "tests" --color "FBCA04" --description "Suíte de testes automatizados" --force
gh label create "documentation" --color "0075CA" --description "Documentação técnica e TCC" --force
gh label create "dependencies" --color "0366D6" --description "Atualizações de dependências (Dependabot)" --force
gh label create "triage" --color "D93F0B" --description "Aguardando triagem inicial" --force
gh label create "stale" --color "EDEDED" --description "Item sem atividade recente" --force
gh label create "pinned" --color "0052CC" --description "Isento de encerramento automático (stale)" --force
gh label create "tcc" --color "7057FF" --description "Escopo de demonstração do TCC" --force
gh label create "ignore-for-release" --color "CFD3D7" --description "Omitir das notas automáticas de release" --force
```

---

## 6. Permissões Gerais de Actions

Acesse **Settings → Actions → General**:
- **Actions permissions:** *Allow all actions and reusable workflows*.
- **Workflow permissions:** selecione **Read repository contents and packages permissions** *(como nossos workflows declaram `permissions` granulares por job, o padrão restritivo reforça a postura de menor privilégio)*.
- Habilite **Allow GitHub Actions to create and approve pull requests** somente se desejar que bots externos abram PRs (não é necessário para o Dependabot, que já possui permissão nativa).
