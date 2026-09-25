from datetime import datetime

from pydantic import BaseModel


class MensagemCriar(BaseModel):
    lead_id: str
    canal_origem: str
    mensagem: str
    status: str = "aguardando_resposta"


class MensagemResposta(BaseModel):
    id: int
    lead_id: str
    canal_origem: str
    mensagem: str
    status: str
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class StatusResposta(BaseModel):
    lead_id: str
    status: str


class StatusAtualizar(BaseModel):
    status: str


class EnviarCanal(BaseModel):
    lead_id: str
    mensagem: str
