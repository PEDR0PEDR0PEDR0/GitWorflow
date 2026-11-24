"""Exceções de domínio do pacote ``calculadora``."""

from __future__ import annotations


class CalculadoraError(ValueError):
    """Exceção base para erros de domínio da calculadora.

    Herda de :class:`ValueError` para manter compatibilidade com
    validações padrão do Python e testes anteriores do projeto.
    """


class DivisaoPorZeroError(CalculadoraError):
    """Erro lançado quando ocorre uma divisão ou módulo por zero."""


class RaizNegativaError(CalculadoraError):
    """Erro lançado ao tentar calcular raiz quadrada real de número negativo."""


class DominioInvalidoError(CalculadoraError):
    """Erro lançado quando argumentos estão fora do domínio matemático suportado."""


class DadosVaziosError(CalculadoraError):
    """Erro lançado ao solicitar cálculos estatísticos sobre coleções vazias."""
