## Descrição

<!-- Resuma o que foi alterado e qual problema ou requisito do TCC esta mudança atende. -->

## Tipo de Mudança

- [ ] `feat`: Nova funcionalidade
- [ ] `fix`: Correção de bug
- [ ] `docs`: Atualização de documentação
- [ ] `ci`: Alteração em workflows ou automações do GitHub Actions
- [ ] `refactor`: Refatoração sem alteração funcional
- [ ] `test`: Adição ou melhoria de testes
- [ ] `chore`: Manutenção, dependências ou configuração

## Issue Relacionada

<!-- Use palavras-chave do GitHub para fechamento automático no merge: Closes #123 -->
Closes #

## Como Testar

<!-- Descreva os comandos executados para validar esta alteração localmente. -->
```bash
ruff check .
mypy calculadora tests scripts
python -m pytest -v --cov=calculadora
```

## Checklist de Qualidade e GitHub Flow

- [ ] O título do PR segue o padrão **Conventional Commits** (ex.: `feat(cli): adiciona comando fatorial`).
- [ ] A branch segue o padrão recomendado (`feat/*`, `fix/*`, `docs/*`, `ci/*`, etc.).
- [ ] Os testes unitários/CLI foram adicionados ou atualizados e a cobertura permanece ≥ 90%.
- [ ] Lint (`ruff`), tipagem (`mypy`) e validação de `.github/` (`scripts/validate_workflows.py`) passaram localmente.
- [ ] Documentação (`README.md`, `CHANGELOG.md` ou `docs/`) atualizada quando aplicável.
- [ ] Nenhum segredo, token ou arquivo temporário foi incluído no commit.
