from contextlib import asynccontextmanager
# from typing import Any, Dict

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
import uvicorn

from db import engine, get_session
from schemas import GutachtenInput, GutachenOutput, Gutachten

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

@app.get("/api/gutachten")
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

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)