from __future__ import annotations
from functools import lru_cache
from discworld_cli.config.settings import get_settings
from discworld_cli.infrastructure.factory import make_repositories, Repositories
from discworld_cli.application.services import CatalogService


@lru_cache(maxsize=1)
def get_repositories() -> Repositories:
    settings = get_settings()
    backend = "sqlite" if settings.backend == "sqlite" else "json"
    return make_repositories(
        backend=backend, sqlite_path=settings.sqlite_path, json_dir=settings.json_dir
    )


@lru_cache(maxsize=1)
def get_catalog_service() -> CatalogService:
    repos = get_repositories()
    return CatalogService(repos.books, repos.characters, repos.mappings)
