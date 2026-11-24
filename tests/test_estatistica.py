"""Testes unitários das funções estatísticas da calculadora."""

from __future__ import annotations

import math

import pytest

from calculadora import (
    DadosVaziosError,
    DominioInvalidoError,
    desvio_padrao,
    media,
    mediana,
    resumo_estatistico,
)

pytestmark = pytest.mark.unit


def test_media() -> None:
    assert media([10, 20, 30]) == 20.0
    assert media([-5, 5]) == 0.0


def test_mediana_impar_e_par() -> None:
    assert mediana([30, 10, 20]) == 20.0
    assert mediana([10, 20, 30, 40]) == 25.0


def test_desvio_padrao_populacional_e_amostral() -> None:
    assert math.isclose(desvio_padrao([2, 4, 4, 4, 5, 5, 7, 9]), 2.0)
    assert math.isclose(desvio_padrao([10, 20, 30], amostral=True), 10.0)


def test_resumo_estatistico() -> None:
    resumo = resumo_estatistico([10, 20, 30, 40])
    assert resumo.quantidade == 4
    assert resumo.soma == 100.0
    assert resumo.media == 25.0
    assert resumo.mediana == 25.0
    assert resumo.minimo == 10.0
    assert resumo.maximo == 40.0
    assert math.isclose(resumo.desvio_padrao, math.sqrt(125.0))

    dados = resumo.para_dict()
    assert dados["quantidade"] == 4
    assert dados["media"] == 25.0


def test_estatistica_erros() -> None:
    with pytest.raises(DadosVaziosError):
        media([])
    with pytest.raises(DadosVaziosError):
        mediana([])
    with pytest.raises(DadosVaziosError):
        desvio_padrao([])
    with pytest.raises(DadosVaziosError):
        resumo_estatistico([])
    with pytest.raises(DominioInvalidoError):
        desvio_padrao([42], amostral=True)
