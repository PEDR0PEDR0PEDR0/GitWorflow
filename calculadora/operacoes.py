"""Operações matemáticas fundamentais com validação e tipagem estrita."""

from __future__ import annotations

import math
from typing import TypeAlias

from calculadora.excecoes import (
    DivisaoPorZeroError,
    DominioInvalidoError,
    RaizNegativaError,
)

Numero: TypeAlias = int | float


def somar(a: Numero, b: Numero) -> Numero:
    """Retorna a soma de ``a`` e ``b``."""
    return a + b


def subtrair(a: Numero, b: Numero) -> Numero:
    """Retorna a diferença ``a - b``."""
    return a - b


def multiplicar(a: Numero, b: Numero) -> Numero:
    """Retorna o produto ``a * b``."""
    return a * b


def dividir(a: Numero, b: Numero) -> float:
    """Retorna o quociente ``a / b``.

    Raises:
        DivisaoPorZeroError: Se ``b`` for igual a zero.
    """
    if b == 0:
        raise DivisaoPorZeroError("Divisão por zero não é permitida")
    return a / b


def potencia(base: Numero, expoente: Numero) -> float:
    """Retorna ``base`` elevada a ``expoente`` no conjunto dos reais.

    Raises:
        DivisaoPorZeroError: Se ``base == 0`` e ``expoente < 0``.
        DominioInvalidoError: Se ``base < 0`` e ``expoente`` não for inteiro.
    """
    if base == 0 and expoente < 0:
        raise DivisaoPorZeroError("Zero elevado a expoente negativo gera divisão por zero")
    if base < 0 and not float(expoente).is_integer():
        raise DominioInvalidoError(
            "Base negativa com expoente fracionário não produz resultado real"
        )
    return float(base**expoente)


def raiz_quadrada(valor: Numero) -> float:
    """Retorna a raiz quadrada real de ``valor``.

    Raises:
        RaizNegativaError: Se ``valor`` for negativo.
    """
    if valor < 0:
        raise RaizNegativaError("Raiz quadrada de número negativo não é permitida nos reais")
    return math.sqrt(valor)


def modulo(a: Numero, b: Numero) -> Numero:
    """Retorna o resto da divisão ``a % b``.

    Raises:
        DivisaoPorZeroError: Se ``b`` for igual a zero.
    """
    if b == 0:
        raise DivisaoPorZeroError("Módulo por zero não é permitido")
    return a % b


def porcentagem(valor: Numero, percentual: Numero) -> float:
    """Calcula ``percentual``% de ``valor``."""
    return (valor * percentual) / 100.0


def fatorial(n: int) -> int:
    """Calcula o fatorial ``n!`` para inteiros não negativos.

    Raises:
        DominioInvalidoError: Se ``n`` for booleano, não inteiro ou negativo.
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise DominioInvalidoError("Fatorial exige um número inteiro não negativo")
    return math.factorial(n)
