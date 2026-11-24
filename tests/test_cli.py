"""Testes da interface de linha de comando (CLI)."""

from __future__ import annotations

import io
import json

import pytest

from calculadora import __version__
from calculadora.cli import executar

pytestmark = pytest.mark.cli


@pytest.mark.parametrize(
    ("argv", "esperado"),
    [
        (["somar", "2", "3"], "5"),
        (["subtrair", "10", "4"], "6"),
        (["multiplicar", "3", "7"], "21"),
        (["dividir", "10", "4"], "2.5"),
        (["potencia", "2", "5"], "32"),
        (["modulo", "10", "3"], "1"),
        (["porcentagem", "200", "25"], "50"),
        (["raiz", "16"], "4"),
        (["fatorial", "5"], "120"),
    ],
)
def test_cli_operacoes_texto(argv: list[str], esperado: str) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    codigo = executar(argv, stdout=stdout, stderr=stderr)

    assert codigo == 0
    assert stdout.getvalue().strip() == esperado
    assert stderr.getvalue() == ""


def test_cli_saida_json() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    codigo = executar(["--json", "somar", "7", "8"], stdout=stdout, stderr=stderr)

    assert codigo == 0
    dados = json.loads(stdout.getvalue())
    assert dados["operacao"] == "somar"
    assert dados["resultado"] == 15.0


def test_cli_estatistica_texto_e_json() -> None:
    stdout = io.StringIO()
    codigo = executar(["estatistica", "10", "20", "30"], stdout=stdout)
    assert codigo == 0
    assert "media=20" in stdout.getvalue()

    stdout_json = io.StringIO()
    codigo_json = executar(
        ["--json", "estatistica", "--amostral", "10", "20", "30"],
        stdout=stdout_json,
    )
    assert codigo_json == 0
    payload = json.loads(stdout_json.getvalue())
    assert payload["amostral"] is True
    assert payload["resultado"]["desvio_padrao"] == pytest.approx(10.0)


def test_cli_erro_dominio_texto_e_json() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    codigo = executar(["dividir", "10", "0"], stdout=stdout, stderr=stderr)
    assert codigo == 1
    assert "Divisão por zero" in stderr.getvalue()

    stdout_json = io.StringIO()
    stderr_json = io.StringIO()
    codigo_json = executar(["--json", "raiz", "-9"], stdout=stdout_json, stderr=stderr_json)
    assert codigo_json == 1
    erro = json.loads(stderr_json.getvalue())
    assert "Raiz quadrada" in erro["erro"]


def test_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        executar(["--version"])
    assert exc_info.value.code == 0
    capturado = capsys.readouterr()
    assert __version__ in capturado.out
