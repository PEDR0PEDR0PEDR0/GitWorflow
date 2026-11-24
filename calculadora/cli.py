"""Interface de linha de comando (CLI) da calculadora."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Sequence
from typing import TextIO

from calculadora import __version__
from calculadora.estatistica import resumo_estatistico
from calculadora.excecoes import CalculadoraError
from calculadora.operacoes import (
    Numero,
    dividir,
    fatorial,
    modulo,
    multiplicar,
    porcentagem,
    potencia,
    raiz_quadrada,
    somar,
    subtrair,
)

OperacaoBinaria = Callable[[Numero, Numero], Numero]

OPERACOES_BINARIAS: dict[str, tuple[str, OperacaoBinaria]] = {
    "somar": ("Soma dois números (a + b)", somar),
    "subtrair": ("Subtrai o segundo número do primeiro (a - b)", subtrair),
    "multiplicar": ("Multiplica dois números (a * b)", multiplicar),
    "dividir": ("Divide o primeiro número pelo segundo (a / b)", dividir),
    "potencia": ("Calcula a potência (a ** b)", potencia),
    "modulo": ("Calcula o resto da divisão (a %% b)", modulo),
    "porcentagem": ("Calcula b%% de a", porcentagem),
}


def construir_parser() -> argparse.ArgumentParser:
    """Constrói o parser principal da CLI."""
    parser = argparse.ArgumentParser(
        prog="calculadora",
        description="Calculadora em Python — projeto demonstrativo de GitHub Workflow (TCC).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="formato_json",
        help="Formata a saída como JSON estruturado.",
    )

    subparsers = parser.add_subparsers(dest="comando", required=True)

    for nome, (ajuda, _) in OPERACOES_BINARIAS.items():
        sub = subparsers.add_parser(nome, help=ajuda)
        sub.add_argument("a", type=float, help="Primeiro operando.")
        sub.add_argument("b", type=float, help="Segundo operando.")

    sub_raiz = subparsers.add_parser("raiz", help="Calcula a raiz quadrada real de um número.")
    sub_raiz.add_argument("valor", type=float, help="Número não negativo.")

    sub_fat = subparsers.add_parser("fatorial", help="Calcula o fatorial de um inteiro >= 0.")
    sub_fat.add_argument("n", type=int, help="Inteiro não negativo.")

    sub_est = subparsers.add_parser(
        "estatistica",
        help="Calcula estatísticas descritivas para uma lista de números.",
    )
    sub_est.add_argument("valores", type=float, nargs="+", help="Lista de valores numéricos.")
    sub_est.add_argument(
        "--amostral",
        action="store_true",
        help="Usa desvio padrão amostral (n - 1) em vez de populacional.",
    )

    return parser


def _formatar_numero(valor: Numero) -> str:
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return f"{valor:g}" if isinstance(valor, float) else str(valor)


def executar(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Executa a CLI e retorna o código de saída do processo."""
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = construir_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        if args.comando in OPERACOES_BINARIAS:
            _, funcao = OPERACOES_BINARIAS[args.comando]
            resultado: Numero = funcao(args.a, args.b)
            payload: dict[str, object] = {
                "operacao": args.comando,
                "operandos": [args.a, args.b],
                "resultado": resultado,
            }
            texto = _formatar_numero(resultado)
        elif args.comando == "raiz":
            resultado = raiz_quadrada(args.valor)
            payload = {
                "operacao": "raiz",
                "operandos": [args.valor],
                "resultado": resultado,
            }
            texto = _formatar_numero(resultado)
        elif args.comando == "fatorial":
            resultado = fatorial(args.n)
            payload = {
                "operacao": "fatorial",
                "operandos": [args.n],
                "resultado": resultado,
            }
            texto = str(resultado)
        else:
            resumo = resumo_estatistico(args.valores, amostral=args.amostral)
            dados = resumo.para_dict()
            payload = {
                "operacao": "estatistica",
                "amostral": args.amostral,
                "resultado": dados,
            }
            texto = (
                f"quantidade={resumo.quantidade} "
                f"soma={_formatar_numero(resumo.soma)} "
                f"media={_formatar_numero(resumo.media)} "
                f"mediana={_formatar_numero(resumo.mediana)} "
                f"minimo={_formatar_numero(resumo.minimo)} "
                f"maximo={_formatar_numero(resumo.maximo)} "
                f"desvio_padrao={_formatar_numero(resumo.desvio_padrao)}"
            )
    except CalculadoraError as exc:
        if args.formato_json:
            print(json.dumps({"erro": str(exc)}, ensure_ascii=False), file=err)
        else:
            print(f"Erro: {exc}", file=err)
        return 1

    if args.formato_json:
        print(json.dumps(payload, ensure_ascii=False), file=out)
    else:
        print(texto, file=out)
    return 0


def main() -> None:
    """Ponto de entrada registrado em ``pyproject.toml``."""
    raise SystemExit(executar())
