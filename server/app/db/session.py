from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

url = settings.DATABASE_URL
kwargs = {'pool_pre_ping': True}
if url.startswith('sqlite'): kwargs['connect_args'] = {'check_same_thread': False}
engine = create_engine(url, **kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
