from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
import uvicorn

from db import engine, get_session
from schemas import GutachtenInput, GutachenOutput, Gutachten, Theme, ThemeInput, ThemeOutput, GradeInput, GradeOutput, Grade

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Gutachten Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[settings.client_origin_url],
    allow_methods=["GET", "POST", "PUT"], 
    allow_headers=["*"],
    # allow_headers=["Authorization", "Content-Type"],
    max_age=86400,
)

@app.get("/api/gutachten/")
def get_gutachten(session: Session = Depends(get_session)) -> list[GutachenOutput]:
    query = select(Gutachten)
    return session.exec(query).all()

@app.get("/api/gutachten/{ga_id}")
def get_gutachten_by_id(ga_id: str, session: Session = Depends(get_session)):
    ga = session.get(Gutachten, ga_id)

    if ga:
        return ga
    else:
        raise HTTPException(404, f"kein gutachen mit id={id}")

@app.post("/api/gutachten")
def save_gutachten(ga: GutachtenInput, session: Session = Depends(get_session)) -> GutachenOutput:
    new_ga = Gutachten.from_orm(ga)
    session.add(new_ga)
    session.commit()
    session.refresh(new_ga)
    return new_ga

@app.put("/api/gutachten/{ga_id}")
def update_gutachten_by_id(ga_id: str, new_data: GutachtenInput, session: Session = Depends(get_session)) -> GutachenOutput:
    gutachten = session.get(Gutachten, ga_id)
    if gutachten:
        gutachten.ga = new_data.ga
        session.commit()
        return gutachten
    else: 
        raise HTTPException(404, f"kein gutachten mit id={id}")

@app.get("/api/theme")
def get_theme(session: Session = Depends(get_session)) -> List[ThemeOutput]:
    query = select(Theme)
    return session.exec(query).all()

@app.post("/api/theme")
def save_theme(th: ThemeInput, session: Session = Depends(get_session)) -> ThemeOutput:
    new_th = Theme.from_orm(th)
    session.add(new_th)
    session.commit()
    session.refresh(new_th)
    return new_th

@app.put("/api/theme/{theme_id}")
def update_theme_by_id(theme_id: str, new_data: ThemeInput, session: Session = Depends(get_session)) -> ThemeOutput:
    theme = session.get(Theme, theme_id)
    if theme:
        theme.theme = new_data.theme
        theme.differentiation = new_data.differentiation
        theme.color = new_data.color
        session.commit()
        return theme
    else:
        raise HTTPException(404, f"kein ober-/unterpunkt mit id={id}")

@app.post("/api/grade")
def save_grade(gr: GradeInput, session: Session = Depends(get_session)) -> GradeOutput:
    new_gr = Grade.from_orm(gr)
    session.add(new_gr)
    session.commit()
    session.refresh(new_gr)
    return new_gr


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)