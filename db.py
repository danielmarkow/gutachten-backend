from sqlmodel import create_engine, Session

engine = create_engine(
    "sqlite:///gutachten.db?check_same_thread=False",
    echo=True # creates logging output
)

def get_session():
    with Session(engine) as session:
        yield session