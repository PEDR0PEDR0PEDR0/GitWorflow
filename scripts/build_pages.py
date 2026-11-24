"""Gera o portal estático para deploy automatizado no GitHub Pages."""

from __future__ import annotations

import argparse
import html
import json
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path

from calculadora import __version__

WORKFLOWS_CATALOGO: tuple[tuple[str, str, str, str], ...] = (
    (
        "CI",
        ".github/workflows/ci.yml",
        "push, pull_request, workflow_dispatch",
        (
            "Lint/Format (Ruff), Tipagem (Mypy), Matriz OS/Python via Reusable Workflow, "
            "Cobertura >= 90%, Empacotamento e Gate obrigatório `testes`."
        ),
    ),
    (
        "Reusable Python Checks",
        ".github/workflows/reusable-python-checks.yml",
        "workflow_call",
        (
            "Workflow reutilizável parametrizado com inputs/outputs, "
            "Composite Action local e resumo em Step Summary."
        ),
    ),
    (
        "PR Governance",
        ".github/workflows/pr-governance.yml",
        "pull_request",
        (
            "Validação de título (Conventional Commits), padrão de branch, "
            "auto-labeler por arquivos alterados e métricas de tamanho do PR."
        ),
    ),
    (
        "Security & Supply Chain",
        ".github/workflows/security.yml",
        "push, pull_request, schedule, workflow_dispatch",
        (
            "Análise SAST com CodeQL e Bandit, auditoria de vulnerabilidades (pip-audit) "
            "e Dependency Review em Pull Requests."
        ),
    ),
    (
        "CD GitHub Pages",
        ".github/workflows/cd-pages.yml",
        "push (main), workflow_dispatch",
        (
            "Pipeline de Entrega Contínua multi-ambiente (staging -> github-pages) "
            "publicando este portal e o relatório HTML de cobertura."
        ),
    ),
    (
        "Release & Attestation",
        ".github/workflows/release.yml",
        "push (tags v*.*.*), workflow_dispatch",
        (
            "Build de wheel/sdist, validação Twine, SHA256SUMS, "
            "Build Provenance Attestation e GitHub Release com notas automáticas."
        ),
    ),
    (
        "Maintenance",
        ".github/workflows/maintenance.yml",
        "schedule (semanal), workflow_dispatch",
        (
            "Verificação periódica de saúde da base de testes e triagem automática "
            "de Issues/PRs inativos (actions/stale)."
        ),
    ),
)


def ler_cobertura(caminho_json: Path | None) -> tuple[str, int, int]:
    """Lê o percentual de cobertura a partir de um arquivo JSON gerado pelo pytest-cov."""
    if caminho_json is None or not caminho_json.is_file():
        return ("N/D", 0, 0)

    dados = json.loads(caminho_json.read_text(encoding="utf-8"))
    totais = dados.get("totals", {})
    percentual = str(totais.get("percent_covered_display", "0"))
    cobertas = int(totais.get("covered_lines", 0))
    total_linhas = int(totais.get("num_statements", 0))
    return (f"{percentual}%", cobertas, total_linhas)


def renderizar_html(
    *,
    versao: str,
    ambiente: str,
    sha: str,
    branch: str,
    repositorio: str,
    run_id: str,
    cobertura_texto: str,
    linhas_cobertas: int,
    total_linhas: int,
    possui_relatorio_cobertura: bool,
    gerado_em: str,
) -> str:
    """Renderiza o documento HTML principal do portal do projeto."""
    sha_curto = html.escape(sha[:7] if sha else "local")
    repo_esc = html.escape(repositorio)
    branch_esc = html.escape(branch)
    ambiente_esc = html.escape(ambiente)
    versao_esc = html.escape(versao)
    cobertura_esc = html.escape(cobertura_texto)
    gerado_esc = html.escape(gerado_em)

    link_run = (
        f"https://github.com/{repo_esc}/actions/runs/{html.escape(run_id)}"
        if run_id.isdigit()
        else f"https://github.com/{repo_esc}/actions"
    )
    bloco_cobertura = (
        '<a class="btn primary" href="./coverage/index.html">Abrir Relatório HTML de Cobertura</a>'
        if possui_relatorio_cobertura
        else (
            '<span class="pill muted">'
            "Relatório HTML de cobertura não anexado nesta build local</span>"
        )
    )

    linhas_tabela = []
    for nome, arquivo, gatilhos, descricao in WORKFLOWS_CATALOGO:
        linhas_tabela.append(
            "<tr>"
            f"<td><strong>{html.escape(nome)}</strong><br><code>{html.escape(arquivo)}</code></td>"
            f"<td><code>{html.escape(gatilhos)}</code></td>"
            f"<td>{html.escape(descricao)}</td>"
            "</tr>"
        )
    corpo_tabela = "\n".join(linhas_tabela)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GitWorflow — Portal CI/CD &amp; Qualidade (TCC)</title>
  <style>
    :root {{
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --muted: #8b949e;
      --accent: #2f81f7;
      --green: #3fb950;
      --purple: #a371f7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }}
    .container {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 2rem 1.25rem 4rem;
    }}
    header {{
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.5rem;
      margin-bottom: 2rem;
    }}
    .eyebrow {{
      display: inline-block;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--green);
      background: rgba(63, 185, 80, 0.12);
      border: 1px solid rgba(63, 185, 80, 0.35);
      border-radius: 999px;
      padding: 0.2rem 0.75rem;
      margin-bottom: 0.75rem;
    }}
    h1 {{ margin: 0 0 0.5rem; font-size: 2rem; }}
    h2 {{ margin: 2.25rem 0 1rem; font-size: 1.35rem; }}
    p.lead {{ color: var(--muted); max-width: 72ch; margin: 0 0 1.25rem; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; }}
    .btn {{
      display: inline-block;
      text-decoration: none;
      padding: 0.55rem 1rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      color: var(--text);
      background: var(--surface);
      font-weight: 600;
      font-size: 0.9rem;
    }}
    .btn.primary {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 1rem;
      margin: 1.5rem 0;
    }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.1rem 1.25rem;
    }}
    .card .label {{ font-size: 0.8rem; color: var(--muted); text-transform: uppercase; }}
    .card .value {{ font-size: 1.65rem; font-weight: 700; margin-top: 0.25rem; }}
    .card .sub {{ font-size: 0.85rem; color: var(--muted); margin-top: 0.25rem; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
    }}
    th, td {{
      text-align: left;
      padding: 0.85rem 1rem;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
      font-size: 0.92rem;
    }}
    th {{ background: rgba(110, 118, 129, 0.12); color: var(--muted); font-weight: 600; }}
    tr:last-child td {{ border-bottom: none; }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.85em;
      background: rgba(110, 118, 129, 0.2);
      padding: 0.15rem 0.35rem;
      border-radius: 4px;
    }}
    .calc-box {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      align-items: center;
      margin-top: 0.75rem;
    }}
    input, select, button {{
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.5rem 0.75rem;
      font-size: 0.95rem;
    }}
    button {{
      cursor: pointer;
      background: var(--purple);
      border-color: var(--purple);
      font-weight: 600;
    }}
    .pill {{
      display: inline-block;
      font-size: 0.85rem;
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      background: var(--surface);
      border: 1px solid var(--border);
    }}
    .pill.muted {{ color: var(--muted); }}
    footer {{
      margin-top: 3rem;
      padding-top: 1.25rem;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 0.85rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 0.5rem;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="eyebrow">TCC · Implementação Completa de GitHub Workflow</span>
      <h1>GitWorflow — Portal de Engenharia &amp; Qualidade</h1>
      <p class="lead">
        Artefato publicado automaticamente pelo pipeline de Entrega Contínua (CD) no GitHub Pages,
        demonstrando GitHub Flow, GitHub Actions, Reusable Workflows, Composite Actions,
        Environments, Segurança DevSecOps e Releases verificadas com Attestation.
      </p>
      <div class="actions">
        {bloco_cobertura}
        <a class="btn" href="https://github.com/{repo_esc}">Repositório no GitHub</a>
        <a class="btn" href="{link_run}">Ver Execução no Actions</a>
      </div>
    </header>

    <section class="grid" aria-label="Indicadores da Build">
      <div class="card">
        <div class="label">Versão do Pacote</div>
        <div class="value">v{versao_esc}</div>
        <div class="sub">Pacote <code>gitworflow-calculadora</code></div>
      </div>
      <div class="card">
        <div class="label">Cobertura de Testes</div>
        <div class="value">{cobertura_esc}</div>
        <div class="sub">{linhas_cobertas} / {total_linhas} linhas cobertas</div>
      </div>
      <div class="card">
        <div class="label">Workflows Ativos</div>
        <div class="value">{len(WORKFLOWS_CATALOGO)}</div>
        <div class="sub">CI, Reusable, Governança, Segurança, CD, Release, Manutenção</div>
      </div>
      <div class="card">
        <div class="label">Ambiente &amp; Revisão</div>
        <div class="value">{ambiente_esc}</div>
        <div class="sub">Branch <code>{branch_esc}</code> · Commit <code>{sha_curto}</code></div>
      </div>
    </section>

    <section>
      <h2>Catálogo de Workflows Implementados</h2>
      <table>
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Gatilhos</th>
            <th>Responsabilidade &amp; Recursos GitHub Actions</th>
          </tr>
        </thead>
        <tbody>
          {corpo_tabela}
        </tbody>
      </table>
    </section>

    <section class="card" style="margin-top: 2rem;">
      <h2 style="margin-top: 0;">Demonstração Interativa (Espelho da CLI)</h2>
      <p style="color: var(--muted); margin-top: 0;">
        Teste rápido no navegador ou execute localmente via
        <code>calculadora somar 2 3 --json</code>.
      </p>
      <div class="calc-box">
        <input id="op-a" type="number" step="any" value="10" aria-label="Primeiro operando">
        <select id="op-fn" aria-label="Operação">
          <option value="somar">+ somar</option>
          <option value="subtrair">- subtrair</option>
          <option value="multiplicar">&times; multiplicar</option>
          <option value="dividir">÷ dividir</option>
          <option value="potencia">^ potencia</option>
          <option value="porcentagem">% porcentagem</option>
        </select>
        <input id="op-b" type="number" step="any" value="5" aria-label="Segundo operando">
        <button id="op-run" type="button">Calcular</button>
        <span id="op-out" class="pill">Resultado: 15</span>
      </div>
    </section>

    <footer>
      <span>Repositório: <code>{repo_esc}</code></span>
      <span>Gerado em {gerado_esc}</span>
    </footer>
  </div>

  <script>
    const btn = document.getElementById("op-run");
    const out = document.getElementById("op-out");
    btn.addEventListener("click", () => {{
      const a = Number(document.getElementById("op-a").value);
      const b = Number(document.getElementById("op-b").value);
      const fn = document.getElementById("op-fn").value;
      let res;
      if (fn === "somar") res = a + b;
      else if (fn === "subtrair") res = a - b;
      else if (fn === "multiplicar") res = a * b;
      else if (fn === "dividir") res = b === 0 ? "Erro: divisão por zero" : a / b;
      else if (fn === "potencia") res = Math.pow(a, b);
      else if (fn === "porcentagem") res = (a * b) / 100;
      out.textContent = "Resultado: " + res;
    }});
  </script>
</body>
</html>
"""


def construir_site(
    *,
    diretorio_saida: Path,
    diretorio_cobertura_html: Path | None = None,
    arquivo_cobertura_json: Path | None = None,
    ambiente: str = "local",
) -> Path:
    """Constrói o diretório estático completo para publicação no GitHub Pages."""
    if diretorio_saida.exists():
        shutil.rmtree(diretorio_saida)
    diretorio_saida.mkdir(parents=True, exist_ok=True)

    possui_relatorio = False
    if diretorio_cobertura_html is not None and diretorio_cobertura_html.is_dir():
        shutil.copytree(diretorio_cobertura_html, diretorio_saida / "coverage")
        possui_relatorio = (diretorio_saida / "coverage" / "index.html").is_file()

    cobertura_texto, linhas_cobertas, total_linhas = ler_cobertura(arquivo_cobertura_json)

    conteudo = renderizar_html(
        versao=__version__,
        ambiente=ambiente,
        sha=os.environ.get("GITHUB_SHA", "localdev"),
        branch=os.environ.get("GITHUB_REF_NAME", "local"),
        repositorio=os.environ.get("GITHUB_REPOSITORY", "PEDR0PEDR0PEDR0/GitWorflow"),
        run_id=os.environ.get("GITHUB_RUN_ID", ""),
        cobertura_texto=cobertura_texto,
        linhas_cobertas=linhas_cobertas,
        total_linhas=total_linhas,
        possui_relatorio_cobertura=possui_relatorio,
        gerado_em=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )

    index_path = diretorio_saida / "index.html"
    index_path.write_text(conteudo, encoding="utf-8")
    (diretorio_saida / ".nojekyll").write_text("", encoding="utf-8")
    return index_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera o portal estático para o GitHub Pages.")
    parser.add_argument("--output", type=Path, default=Path("_site"))
    parser.add_argument("--coverage-html", type=Path, default=Path("site_cov"))
    parser.add_argument("--coverage-json", type=Path, default=Path("coverage.json"))
    parser.add_argument(
        "--environment",
        default=os.environ.get("DEPLOY_ENV", "local"),
    )
    args = parser.parse_args()

    index_path = construir_site(
        diretorio_saida=args.output,
        diretorio_cobertura_html=args.coverage_html if args.coverage_html.exists() else None,
        arquivo_cobertura_json=args.coverage_json if args.coverage_json.exists() else None,
        ambiente=args.environment,
    )
    print(f"Portal estático gerado com sucesso em: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
