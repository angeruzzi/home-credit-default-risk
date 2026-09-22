"""Utilitários compartilhados do projeto Home Credit Default Risk."""

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Diretórios utilizados pelo projeto."""

    project_root: Path
    data_root: Path
    data_raw: Path
    data_interim: Path
    data_processed: Path
    artifacts_root: Path
    models: Path
    preprocessing: Path
    metadata: Path
    reports_root: Path
    figures: Path
    tables: Path
    docs: Path


def is_google_colab() -> bool:
    """Indica se o código está sendo executado no Google Colab."""
    return "google.colab" in sys.modules


def setup_project(
    use_google_drive_cache: bool = True,
    mount_google_drive: bool = True,
) -> ProjectPaths:
    """
    Configura os diretórios do projeto.

    No Google Colab, pode utilizar o Google Drive como cache persistente.
    Em outros ambientes, utiliza os diretórios locais do repositório.

    Parameters
    ----------
    use_google_drive_cache:
        Define se dados e artefatos serão armazenados no Google Drive
        quando a execução ocorrer no Colab.

    mount_google_drive:
        Define se a função deve montar o Google Drive automaticamente.

    Returns
    -------
    ProjectPaths
        Objeto contendo todos os caminhos utilizados pelo projeto.
    """
    project_root = Path(__file__).resolve().parent
    in_colab = is_google_colab()

    if in_colab and use_google_drive_cache:
        if mount_google_drive:
            from google.colab import drive

            drive.mount(
                "/content/drive",
                force_remount=False,
            )

        cache_root = Path(
            "/content/drive/MyDrive/home-credit-default-risk"
        )

        data_root = cache_root / "data"
        artifacts_root = cache_root / "artifacts"

    else:
        data_root = project_root / "data"
        artifacts_root = project_root / "artifacts"

    paths = ProjectPaths(
        project_root=project_root,
        data_root=data_root,
        data_raw=data_root / "raw",
        data_interim=data_root / "interim",
        data_processed=data_root / "processed",
        artifacts_root=artifacts_root,
        models=artifacts_root / "models",
        preprocessing=artifacts_root / "preprocessing",
        metadata=artifacts_root / "metadata",
        reports_root=project_root / "reports",
        figures=project_root / "reports" / "figures",
        tables=project_root / "reports" / "tables",
        docs=project_root / "docs",
    )

    directories = [
        paths.data_raw,
        paths.data_interim,
        paths.data_processed,
        paths.models,
        paths.preprocessing,
        paths.metadata,
        paths.figures,
        paths.tables,
        paths.docs,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    storage_mode = (
        "Google Drive"
        if in_colab and use_google_drive_cache
        else "armazenamento local"
    )

    print(f"Ambiente Colab: {in_colab}")
    print(f"Modo de armazenamento: {storage_mode}")
    print(f"Raiz do projeto: {paths.project_root}")
    print(f"Dados: {paths.data_root}")
    print(f"Artefatos: {paths.artifacts_root}")
    print(f"Relatórios: {paths.reports_root}")

    return paths