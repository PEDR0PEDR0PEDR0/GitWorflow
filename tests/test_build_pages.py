"""Testes para o script de geração do portal estático do GitHub Pages."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_pages import construir_site, ler_cobertura

pytestmark = pytest.mark.pages


def test_construir_site_com_cobertura(tmp_path: Path) -> None:
    cov_html = tmp_path / "cov_html"
    cov_html.mkdir()
    (cov_html / "index.html").write_text("<html><body>Coverage</body></html>", encoding="utf-8")

    cov_json = tmp_path / "coverage.json"
    cov_json.write_text(
        json.dumps(
            {
                "totals": {
                    "percent_covered_display": "98",
                    "covered_lines": 120,
                    "num_statements": 122,
                }
            }
        ),
        encoding="utf-8",
    )

    saida = tmp_path / "_site"
    index = construir_site(
        diretorio_saida=saida,
        diretorio_cobertura_html=cov_html,
        arquivo_cobertura_json=cov_json,
        ambiente="staging",
    )

    assert index.is_file()
    assert (saida / ".nojekyll").is_file()
    assert (saida / "coverage" / "index.html").is_file()

    conteudo = index.read_text(encoding="utf-8")
    assert "98%" in conteudo
    assert "staging" in conteudo
    assert "Abrir Relatório HTML de Cobertura" in conteudo


def test_ler_cobertura_ausente(tmp_path: Path) -> None:
    percentual, cobertas, total = ler_cobertura(tmp_path / "inexistente.json")
    assert percentual == "N/D"
    assert cobertas == 0
    assert total == 0
