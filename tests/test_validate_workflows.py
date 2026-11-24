"""Testes do validador estrutural e de segurança dos workflows em ``.github/``."""

from __future__ import annotations

from pathlib import Path

from scripts.validate_workflows import validar_diretorio_github, validar_workflow


def test_diretorio_github_do_projeto_e_valido() -> None:
    assert validar_diretorio_github() == []


def test_detecta_falhas_estruturais_e_script_injection(tmp_path: Path) -> None:
    wf_invalido = {
        "on": {"pull_request": {}},
        "jobs": {
            "inseguro": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Echo perigoso",
                        "run": 'echo "${{ github.event.pull_request.title }}"',
                    }
                ],
            }
        },
    }

    erros = validar_workflow(tmp_path / "bad.yml", wf_invalido, raiz=tmp_path)
    mensagens = "\n".join(erros)

    assert "name" in mensagens
    assert "concurrency" in mensagens
    assert "timeout-minutes" in mensagens
    assert "permissions" in mensagens
    assert "env:" in mensagens
