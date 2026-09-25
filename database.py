import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------------------------------------
# Carrega as variaveis do arquivo .env (na mesma pasta) para o
# ambiente do processo, se ainda nao estiverem definidas. Assim
# nao e mais necessario rodar $env:DATABASE_URL=... manualmente
# a cada terminal novo.
# ------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------
# String de conexao ao Postgres. Lida do arquivo .env (variavel
# DATABASE_URL), por exemplo:
#   postgresql://usuario:senha@host:5432/nome_do_banco
#
# Se estiver usando Supabase, a string de conexao esta em:
# Project Settings > Database > Connection string > URI
# ------------------------------------------------------------
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/crm_ia"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
