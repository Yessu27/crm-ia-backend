from sqlalchemy import Column, Integer, String, Text, DateTime, func

from database import Base


class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String(100), nullable=False, index=True)
    canal_origem = Column(String(50), nullable=False)
    mensagem = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="aguardando_resposta", index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
