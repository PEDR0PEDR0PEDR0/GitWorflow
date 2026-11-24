# Política de Segurança

## Versões Suportadas

| Versão | Suporte de Segurança |
| :--- | :--- |
| `1.x` | Ativo |
| `< 1.0` | Sem suporte |

## Controles Automatizados no Repositório

Este projeto implementa múltiplas camadas de segurança de engenharia e cadeia de suprimentos (DevSecOps):

- **Análise Estática (SAST):** GitHub CodeQL (`security-extended`) e Bandit executados em PRs, pushes na `main` e semanalmente via `schedule`.
- **Auditoria de Dependências:** `pip-audit` e `actions/dependency-review-action` bloqueiam vulnerabilidades de severidade alta em Pull Requests.
- **Atualizações Contínuas:** Dependabot configurado para ecossistemas `pip` e `github-actions` (`.github/dependabot.yml`).
- **Princípio do Privilégio Mínimo:** todos os workflows declaram `permissions` explícitas, passam dados de PR por variáveis de ambiente (`env:`) para evitar *script injection* e evitam `pull_request_target` com checkout não confiável.
- **Integridade de Artefatos:** releases oficiais geram `SHA256SUMS.txt` e **Build Provenance Attestation** (`actions/attest-build-provenance`).

## Como Reportar uma Vulnerabilidade

**Não abra issues públicas para relatar falhas de segurança.**

1. Utilize o recurso **Private Vulnerability Reporting** na aba **Security → Advisories** do repositório no GitHub.
2. Inclua descrição da vulnerabilidade, impacto estimado, passos para reprodução e, se possível, sugestão de correção.
3. O mantenedor responderá em até **5 dias úteis** com avaliação inicial e plano de remediação.
