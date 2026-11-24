"""Pacote ``calculadora`` — base Python para demonstração completa de GitHub Workflow."""

from __future__ import annotations

__version__ = "1.0.0"

from calculadora.estatistica import (
    ResumoEstatistico,
    desvio_padrao,
    media,
    mediana,
    resumo_estatistico,
)
from calculadora.excecoes import (
    CalculadoraError,
    DadosVaziosError,
    DivisaoPorZeroError,
    DominioInvalidoError,
    RaizNegativaError,
)
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

__all__ = [
    "CalculadoraError",
    "DadosVaziosError",
    "DivisaoPorZeroError",
    "DominioInvalidoError",
    "Numero",
    "RaizNegativaError",
    "ResumoEstatistico",
    "__version__",
    "desvio_padrao",
    "dividir",
    "fatorial",
    "media",
    "mediana",
    "modulo",
    "multiplicar",
    "porcentagem",
    "potencia",
    "raiz_quadrada",
    "resumo_estatistico",
    "somar",
    "subtrair",
]
