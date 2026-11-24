"""Valida sintaxe e boas práticas estruturais dos arquivos em ``.github/``."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DIR_GITHUB = RAIZ / ".github"

# Contextos controlados por terceiros que nunca devem ser interpolados direto em `run:`
PADRAO_INJECAO_RUN = re.compile(
    r"\$\{\{\s*github\.event\.(pull_request\.(title|body)|issue\.(title|body)|comment\.body)"
)


def validar_workflow(caminho: Path, dados: dict[Any, Any], *, raiz: Path = RAIZ) -> list[str]:
    """Valida regras estruturais e de segurança de um arquivo de workflow."""
    erros: list[str] = []
    rel = caminho.relative_to(raiz) if caminho.is_relative_to(raiz) else caminho

    if "name" not in dados:
        erros.append(f"{rel}: campo obrigatório 'name' ausente")

    # PyYAML (YAML 1.1) interpreta a chave 'on' sem aspas como booleano True
    gatilhos = dados.get("on", dados.get(True))
    if gatilhos is None:
        erros.append(f"{rel}: campo obrigatório 'on' ausente")

    apenas_reusable = isinstance(gatilhos, dict) and set(gatilhos.keys()) == {"workflow_call"}
    if not apenas_reusable and "concurrency" not in dados:
        erros.append(f"{rel}: workflow deve declarar 'concurrency'")

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
        steps = config_job.get("steps", [])
        if isinstance(steps, list):
            for idx, step in enumerate(steps, start=1):
                if (
                    isinstance(step, dict)
                    and isinstance(step.get("run"), str)
                    and PADRAO_INJECAO_RUN.search(step["run"])
                ):
                    erros.append(
                        f"{rel}: job '{nome_job}' step #{idx} interpola campo não confiável "
                        "diretamente em 'run:' (use variáveis de ambiente em 'env:')"
                    )

    return erros


def validar_diretorio_github(dir_github: Path = DIR_GITHUB) -> list[str]:
    """Executa validação de todos os YAMLs e JSONs em ``.github/``."""
    erros: list[str] = []
    if not dir_github.is_dir():
        return [".github/: diretório não encontrado"]

    raiz_ref = dir_github.parent
    for arquivo in sorted(dir_github.rglob("*")):
        if not arquivo.is_file():
            continue
        rel = arquivo.relative_to(raiz_ref)

        if arquivo.suffix in {".yml", ".yaml"}:
            try:
                conteudo = yaml.safe_load(arquivo.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                erros.append(f"{rel}: erro de sintaxe YAML: {exc}")
                continue
            if not isinstance(conteudo, dict):
                erros.append(f"{rel}: documento YAML deve ser um mapeamento na raiz")
                continue
            if arquivo.parent == dir_github / "workflows":
                erros.extend(validar_workflow(arquivo, conteudo, raiz=raiz_ref))

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
