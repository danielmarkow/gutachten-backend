from sqlmodel import create_engine, Session

engine = create_engine(
    "sqlite:///gutachten.db",
    echo=True # creates logging output
)

def get_session():
    with Session(engine) as session:
        yield session