"""Параметры запуска."""

from pydantic import (
    BaseModel,
    DirectoryPath,
    FilePath,
)


class Config(BaseModel):
    """Проверенные параметры командной строки."""

    vfs: DirectoryPath | None = None
    script: FilePath | None = None
