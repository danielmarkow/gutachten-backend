# {
#   "root":
#     {
#       "children": [
#         {
#           "children":[
#             {"detail":0,"format":0,"mode":"normal","style":"","text":"hello world","type":"text","version":1}
#           ],"direction":"ltr","format":"","indent":0,"type":"paragraph","version":1},
# {"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"blub","type":"text","version":1}],"direction":"ltr","format":"","indent":0,"type":"paragraph","version":1}],"direction":"ltr","format":"","indent":0,"type":"root","version":1}}
import uuid as uuid_pkg
# from pydantic import BaseModel
from sqlmodel import SQLModel, Field, JSON, Column

class GutachtenInput(SQLModel):
    ga: dict

class GutachenOutput(GutachtenInput):
    id: uuid_pkg.UUID
    ga: dict

class Gutachten(GutachtenInput, table=True):
    id: uuid_pkg.UUID | None = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    ga: dict = Field(sa_column=Column(JSON), default={})