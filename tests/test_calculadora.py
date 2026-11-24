"""Testes unitários das operações matemáticas da calculadora."""

from __future__ import annotations

import math

import pytest

from calculadora import (
    CalculadoraError,
    DivisaoPorZeroError,
    DominioInvalidoError,
    RaizNegativaError,
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

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [
        (2, 3, 5),
        (-2, 3, 1),
        (-5, -7, -12),
        (0, 0, 0),
        (2.5, 1.5, 4.0),
    ],
)
def test_somar(a: float, b: float, esperado: float) -> None:
    assert somar(a, b) == esperado


@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [
        (5, 3, 2),
        (3, 5, -2),
        (-4, -6, 2),
        (2.5, 0.5, 2.0),
    ],
)
def test_subtrair(a: float, b: float, esperado: float) -> None:
    assert subtrair(a, b) == esperado


@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [
        (4, 5, 20),
        (-3, 5, -15),
        (-2, -6, 12),
        (10, 0, 0),
        (1.5, 2, 3.0),
    ],
)
def test_multiplicar(a: float, b: float, esperado: float) -> None:
    assert multiplicar(a, b) == esperado


def test_dividir() -> None:
    assert dividir(10, 2) == 5.0
    assert dividir(-9, 3) == -3.0
    assert math.isclose(dividir(1, 4), 0.25)


def test_dividir_por_zero() -> None:
    with pytest.raises(DivisaoPorZeroError, match="Divisão por zero"):
        dividir(1, 0)
    # Compatibilidade garantida com ValueError (base de CalculadoraError)
    with pytest.raises(ValueError):
        dividir(10, 0)


@pytest.mark.parametrize(
    ("base", "expoente", "esperado"),
    [
        (2, 3, 8.0),
        (5, 0, 1.0),
        (4, 0.5, 2.0),
        (-2, 3, -8.0),
        (2, -2, 0.25),
    ],
)
def test_potencia(base: float, expoente: float, esperado: float) -> None:
    assert math.isclose(potencia(base, expoente), esperado)


def test_potencia_erros_dominio() -> None:
    with pytest.raises(DivisaoPorZeroError):
        potencia(0, -1)
    with pytest.raises(DominioInvalidoError):
        potencia(-4, 0.5)


def test_raiz_quadrada() -> None:
    assert raiz_quadrada(0) == 0.0
    assert raiz_quadrada(9) == 3.0
    assert math.isclose(raiz_quadrada(2), math.sqrt(2))


def test_raiz_quadrada_negativa() -> None:
    with pytest.raises(RaizNegativaError):
        raiz_quadrada(-1)


def test_modulo() -> None:
    assert modulo(10, 3) == 1
    assert modulo(9, 3) == 0


def test_modulo_por_zero() -> None:
    with pytest.raises(DivisaoPorZeroError):
        modulo(10, 0)


def test_porcentagem() -> None:
    assert porcentagem(200, 15) == 30.0
    assert porcentagem(50, 0) == 0.0
    assert porcentagem(80, 125) == 100.0


@pytest.mark.parametrize(
    ("n", "esperado"),
    [
        (0, 1),
        (1, 1),
        (5, 120),
        (6, 720),
    ],
)
def test_fatorial(n: int, esperado: int) -> None:
    assert fatorial(n) == esperado


def test_fatorial_erros_dominio() -> None:
    with pytest.raises(DominioInvalidoError):
        fatorial(-1)
    with pytest.raises(CalculadoraError):
        fatorial(True)
    with pytest.raises(DominioInvalidoError):
        fatorial(3.5)  # type: ignore[arg-type]
