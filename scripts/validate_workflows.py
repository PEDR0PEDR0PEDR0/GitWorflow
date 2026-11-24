"""Valida sintaxe e boas práticas estruturais dos arquivos em ``.github/``."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DIR_GITHUB = RAIZ / ".github"


def _validar_workflow(caminho: Path, dados: dict[Any, Any]) -> list[str]:
    erros: list[str] = []
    rel = caminho.relative_to(RAIZ)

    if "name" not in dados:
        erros.append(f"{rel}: campo obrigatório 'name' ausente")

    # PyYAML (YAML 1.1) interpreta a chave 'on' sem aspas como booleano True
    if "on" not in dados and True not in dados:
        erros.append(f"{rel}: campo obrigatório 'on' ausente")

    jobs = dados.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        erros.append(f"{rel}: seção 'jobs' ausente ou vazia")
        return erros

    workflow_tem_permissions = "permissions" in dados
    for nome_job, config_job in jobs.items():
        if not isinstance(config_job, dict):
            erros.append(f"{rel}: job '{nome_job}' inválido")
            continue
        usa_reusable = "uses" in config_job
        if not usa_reusable and "timeout-minutes" not in config_job:
            erros.append(f"{rel}: job '{nome_job}' deve definir 'timeout-minutes'")
        if not workflow_tem_permissions and "permissions" not in config_job:
            erros.append(
                f"{rel}: job '{nome_job}' (ou workflow) deve declarar 'permissions' explícitas"
            )

    return erros


def validar_diretorio_github() -> list[str]:
    """Executa validação de todos os YAMLs e JSONs em ``.github/``."""
    erros: list[str] = []
    if not DIR_GITHUB.is_dir():
        return [".github/: diretório não encontrado"]

    for arquivo in sorted(DIR_GITHUB.rglob("*")):
        if not arquivo.is_file():
            continue
        rel = arquivo.relative_to(RAIZ)

        if arquivo.suffix in {".yml", ".yaml"}:
            try:
                conteudo = yaml.safe_load(arquivo.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                erros.append(f"{rel}: erro de sintaxe YAML: {exc}")
                continue
            if not isinstance(conteudo, dict):
                erros.append(f"{rel}: documento YAML deve ser um mapeamento na raiz")
                continue
            if arquivo.parent == DIR_GITHUB / "workflows":
                erros.extend(_validar_workflow(arquivo, conteudo))

        elif arquivo.suffix == ".json":
            try:
                json.loads(arquivo.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                erros.append(f"{rel}: erro de sintaxe JSON: {exc}")

    return erros


def main() -> int:
    erros = validar_diretorio_github()
    if erros:
        print("Falhas encontradas na validação de .github/:", file=sys.stderr)
        for erro in erros:
            print(f"  - {erro}", file=sys.stderr)
        return 1

    total_yaml = len(list(DIR_GITHUB.rglob("*.yml"))) + len(list(DIR_GITHUB.rglob("*.yaml")))
    total_json = len(list(DIR_GITHUB.rglob("*.json")))
    print(f"Validação concluída com sucesso: {total_yaml} YAML(s) e {total_json} JSON(s) válidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
