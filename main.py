import secure

from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
import uvicorn
from pydantic import create_model

from db import engine, get_session
from schemas import GutachtenInput, GutachenOutput, Gutachten, Theme, ThemeInput, ThemeOutput, GradeInput, GradeOutput, Grade
from validate import validate

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Gutachten Backend", openapi_url=None, lifespan=lifespan)

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)

@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[settings.client_origin_url],
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    # allow_headers=["*"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=86400,
)

@app.get("/api/gutachten")
def get_gutachten(auth_payload = Depends(validate), session: Session = Depends(get_session)) -> list[GutachenOutput]:
    query = select(Gutachten).where(Gutachten.user_id == auth_payload.get("sub"))
    return session.exec(query).all()

@app.get("/api/gutachten/{ga_id}")
def get_gutachten_by_id(ga_id: str, auth_payload = Depends(validate), session: Session = Depends(get_session)):
    query = select(Gutachten).where(Gutachten.id == ga_id).where(Gutachten.user_id == auth_payload.get("sub"))
    ga = session.exec(query).all()
    if ga:
        return ga
    else:
        raise HTTPException(404, f"kein gutachen mit id={id}")

@app.post("/api/gutachten")
def save_gutachten(ga: GutachtenInput, auth_payload = Depends(validate), session: Session = Depends(get_session)) -> GutachenOutput:
    new_ga = Gutachten.from_orm(ga)
    session.add(new_ga)
    session.commit()
    session.refresh(new_ga)
    return new_ga

@app.put("/api/gutachten/{ga_id}")
def update_gutachten_by_id(ga_id: str, new_data: GutachtenInput, auth_payload = Depends(validate), session: Session = Depends(get_session)) -> GutachenOutput:
    query = select(Gutachten).where(Gutachten.id == ga_id).where(Gutachten.user_id == auth_payload.get("sub"))
    gutachten = session.exec(query).first()
    if gutachten:
        gutachten.ga = new_data.ga
        session.commit()
        return gutachten
    else: 
        raise HTTPException(404, f"kein gutachten mit id={id}")

@app.get("/api/theme")
def get_theme(auth_payload = Depends(validate), session: Session = Depends(get_session)) -> List[ThemeOutput]:
    query = select(Theme).where(Theme.user_id == auth_payload.get("sub"))
    return session.exec(query).all()

@app.post("/api/theme")
def save_theme(th: ThemeInput, auth_payload = Depends(validate), session: Session = Depends(get_session)) -> ThemeOutput:
    new_th = Theme.from_orm(th)
    session.add(new_th)
    session.commit()
    session.refresh(new_th)
    return new_th

@app.put("/api/theme/{theme_id}")
def update_theme_by_id(theme_id: str, new_data: ThemeInput, auth_payload = Depends(validate), session: Session = Depends(get_session)) -> ThemeOutput:
    query = select(Theme).where(Theme.id == theme_id).where(Theme.user_id == auth_payload.get("sub"))
    theme = session.exec(query).all()
    if theme:
        theme[0].theme = new_data.theme
        theme[0].differentiation = new_data.differentiation
        theme[0].color = new_data.color
        session.commit()
        return theme[0]
    else:
        raise HTTPException(404, f"kein ober-/unterpunkt mit id={id}")

@app.delete("/api/theme/{theme_id}", status_code=204)
def delete_theme_by_id(theme_id: str, auth_payload = Depends(validate), session: Session = Depends(get_session)):
    query = select(Theme).where(Theme.id == theme_id).where(Theme.user_id == auth_payload.get("sub"))
    theme = session.exec(query).all()
    if theme:
        session.delete(theme[0])
        session.commit()
    else:
        raise HTTPException(404, f"no theme with id={theme_id}")

@app.post("/api/grade", status_code=204)
def save_grade(gr: List[GradeInput], auth_payload = Depends(validate), session: Session = Depends(get_session)):
    new_gr = [grade.dict() for grade in gr]
    session.bulk_insert_mappings(Grade, new_gr)
    session.commit()

@app.put("/api/grade", status_code=204)
def update_grade(gr: List[GradeOutput], auth_payload = Depends(validate), session: Session = Depends(get_session)):
    updated_gr = [grade.dict() for grade in gr]
    session.bulk_update_mappings(Grade, updated_gr)
    session.commit()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, server_header=False)