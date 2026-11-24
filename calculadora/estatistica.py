"""Funções estatísticas descritivas sobre sequências numéricas."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from calculadora.excecoes import DadosVaziosError, DominioInvalidoError
from calculadora.operacoes import Numero


@dataclass(frozen=True, slots=True)
class ResumoEstatistico:
    """Resumo descritivo de uma coleção numérica."""

    quantidade: int
    soma: float
    media: float
    mediana: float
    minimo: float
    maximo: float
    desvio_padrao: float

    def para_dict(self) -> dict[str, int | float]:
        """Converte o resumo para dicionário serializável em JSON."""
        return {
            "quantidade": self.quantidade,
            "soma": self.soma,
            "media": self.media,
            "mediana": self.mediana,
            "minimo": self.minimo,
            "maximo": self.maximo,
            "desvio_padrao": self.desvio_padrao,
        }


def _validar_nao_vazio(valores: Sequence[Numero]) -> list[float]:
    if not valores:
        raise DadosVaziosError("É necessário informar ao menos um valor numérico")
    return [float(v) for v in valores]


def media(valores: Sequence[Numero]) -> float:
    """Calcula a média aritmética simples."""
    dados = _validar_nao_vazio(valores)
    return sum(dados) / len(dados)


def mediana(valores: Sequence[Numero]) -> float:
    """Calcula a mediana dos valores informados."""
    ordenados = sorted(_validar_nao_vazio(valores))
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 1:
        return ordenados[meio]
    return (ordenados[meio - 1] + ordenados[meio]) / 2.0


def desvio_padrao(valores: Sequence[Numero], *, amostral: bool = False) -> float:
    """Calcula o desvio padrão populacional (padrão) ou amostral."""
    dados = _validar_nao_vazio(valores)
    if amostral and len(dados) < 2:
        raise DominioInvalidoError("Desvio padrão amostral exige ao menos dois valores")
    m = sum(dados) / len(dados)
    divisor = len(dados) - 1 if amostral else len(dados)
    variancia = sum((x - m) ** 2 for x in dados) / divisor
    return math.sqrt(variancia)


def resumo_estatistico(
    valores: Sequence[Numero],
    *,
    amostral: bool = False,
) -> ResumoEstatistico:
    """Gera um :class:`ResumoEstatistico` completo para os valores informados."""
    dados = _validar_nao_vazio(valores)
    return ResumoEstatistico(
        quantidade=len(dados),
        soma=sum(dados),
        media=media(dados),
        mediana=mediana(dados),
        minimo=min(dados),
        maximo=max(dados),
        desvio_padrao=desvio_padrao(dados, amostral=amostral),
    )
