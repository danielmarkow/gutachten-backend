import uuid as uuid_pkg
from typing import Optional
from sqlmodel import SQLModel, Field, JSON, Column

class GutachtenInput(SQLModel):
    ga: dict
    description: Optional[str]

class GutachenOutput(GutachtenInput):
    id: uuid_pkg.UUID
    ga: dict
    description: Optional[str]

class Gutachten(GutachtenInput, table=True):
    id: uuid_pkg.UUID | None = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    ga: dict = Field(sa_column=Column(JSON), default={})
    description: Optional[str] = Field(default=None)

class TextbausteinInput(SQLModel):
    theme: str
    differentiation: str
    grade: int
    snippet: str

class TextbausteinOutput(TextbausteinInput):
    id: uuid_pkg.UUID

class Textbaustein(TextbausteinInput, table=True):
    id: uuid_pkg.UUID | None = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
