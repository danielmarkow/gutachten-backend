import uuid as uuid_pkg
from typing import Optional, List, Union
from sqlmodel import SQLModel, Field, JSON, Column, Relationship


class GutachtenInput(SQLModel):
    ga: dict
    description: Optional[str] = None
    user_id: str


class GutachtenOutput(GutachtenInput):
    id: uuid_pkg.UUID
    ga: dict
    description: Optional[str]


class Gutachten(GutachtenInput, table=True):
    id: Union[uuid_pkg.UUID, None] = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    ga: dict = Field(sa_column=Column(JSON), default={})
    description: Optional[str] = Field(default=None)
    user_id: str = Field(index=True)


# textsnippets
class GradeInput(SQLModel):
    grade: int
    snippet: str
    theme_id: uuid_pkg.UUID
    user_id: str


class GradeOutput(GradeInput):
    id: uuid_pkg.UUID


class Grade(GradeInput, table=True):
    id: Optional[uuid_pkg.UUID] = Field(default_factory=uuid_pkg.uuid4, primary_key=True)
    theme_id: uuid_pkg.UUID = Field(foreign_key="theme.id")
    theme: "Theme" = Relationship(back_populates="grades", sa_relationship_kwargs={"cascade": "delete"})
    user_id: str = Field(index=True)


class ThemeInput(SQLModel):
    theme: str
    differentiation: str
    color: Optional[str]
    user_id: str


class Theme(ThemeInput, table=True):
    id: Optional[uuid_pkg.UUID] = Field(default_factory=uuid_pkg.uuid4, primary_key=True)
    grades: List["Grade"] = Relationship(back_populates="theme", sa_relationship_kwargs={"cascade": "delete"})
    user_id: str = Field(index=True)


class ThemeOutput(ThemeInput):
    id: uuid_pkg.UUID
    user_id: str
    grades: List[GradeOutput] = []
