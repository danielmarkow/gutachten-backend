import uuid as uuid_pkg
from typing import Optional, List
from sqlmodel import SQLModel, Field, JSON, Column, Relationship

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
class GradeInput(SQLModel):
    grade: int
    snippet: str
    theme_id: uuid_pkg.UUID

class GradeOutput(GradeInput):
    id: uuid_pkg.UUID

class Grade(GradeInput, table=True):
    id: uuid_pkg.UUID | None = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    theme_id: uuid_pkg.UUID = Field(foreign_key="theme.id")
    theme: "Theme" = Relationship(back_populates="grades")

class ThemeInput(SQLModel):
    theme: str
    differentiation: str

class Theme(ThemeInput, table=True):
    id: uuid_pkg.UUID | None = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    grades: List["Grade"] = Relationship(back_populates="theme")

class ThemeOutput(ThemeInput):
    id: uuid_pkg.UUID
    grades: List[GradeOutput] = []

# class TextbausteinInput(SQLModel):
#     theme: str
#     differentiation: str
#     grade: int
#     snippet: str

# class TextbausteinOutput(TextbausteinInput):
#     id: uuid_pkg.UUID

# class Textbaustein(TextbausteinInput, table=True):
#     id: uuid_pkg.UUID | None = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
