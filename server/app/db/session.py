import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

url = settings.DATABASE_URL
if url.startswith('postgres://'):
    url = url.replace('postgres://', 'postgresql+psycopg://', 1)
elif url.startswith('postgresql://') and not url.startswith('postgresql+'):
    url = url.replace('postgresql://', 'postgresql+psycopg://', 1)
elif os.environ.get('VERCEL') and url.startswith('sqlite') and not url.startswith('sqlite:////tmp/'):
    url = 'sqlite:////tmp/interviewiq.db'

kwargs = {'pool_pre_ping': True}
if url.startswith('sqlite'): kwargs['connect_args'] = {'check_same_thread': False}
engine = create_engine(url, **kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
