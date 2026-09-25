import logging

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import schemas

# ------------------------------------------------------------
# Cria as tabelas automaticamente se ainda nao existirem
# (equivalente a rodar o schema.sql na primeira vez)
# ------------------------------------------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM IA - Backend de Leads")
logger = logging.getLogger("crm_ia")


# ============================================================
# POST /api/mensagens
# Grava uma nova mensagem recebida (chamado pelo node
# "Grava mensagem no CRM" no n8n)
# ============================================================
@app.post("/api/mensagens", response_model=schemas.MensagemResposta)
def criar_mensagem(dados: schemas.MensagemCriar, db: Session = Depends(get_db)):
    nova_mensagem = models.Mensagem(
        lead_id=dados.lead_id,
        canal_origem=dados.canal_origem,
        mensagem=dados.mensagem,
        status=dados.status,
    )
    db.add(nova_mensagem)
    db.commit()
    db.refresh(nova_mensagem)
    logger.info(f"Mensagem gravada: lead_id={dados.lead_id} canal={dados.canal_origem}")
    return nova_mensagem


# ============================================================
# GET /api/mensagens/{lead_id}/status
# Consulta o status atual da conversa (chamado pelo node
# "Consulta status atual no CRM" no n8n, apos os 5 minutos)
# ============================================================
@app.get("/api/mensagens/{lead_id}/status", response_model=schemas.StatusResposta)
def consultar_status(lead_id: str, db: Session = Depends(get_db)):
    ultima_mensagem = (
        db.query(models.Mensagem)
        .filter(models.Mensagem.lead_id == lead_id)
        .order_by(models.Mensagem.id.desc())
        .first()
    )
    if not ultima_mensagem:
        raise HTTPException(status_code=404, detail=f"Nenhuma mensagem encontrada para lead_id={lead_id}")

    return schemas.StatusResposta(lead_id=lead_id, status=ultima_mensagem.status)


# ============================================================
# PATCH /api/mensagens/{lead_id}/status
# Atualiza o status (chamado pelo node "Atualiza status
# (respondido_por_ia)" no n8n, e tambem deve ser chamado pelo
# seu chat interno quando um humano responde manualmente)
# ============================================================
@app.patch("/api/mensagens/{lead_id}/status", response_model=schemas.StatusResposta)
def atualizar_status(lead_id: str, dados: schemas.StatusAtualizar, db: Session = Depends(get_db)):
    ultima_mensagem = (
        db.query(models.Mensagem)
        .filter(models.Mensagem.lead_id == lead_id)
        .order_by(models.Mensagem.id.desc())
        .first()
    )
    if not ultima_mensagem:
        raise HTTPException(status_code=404, detail=f"Nenhuma mensagem encontrada para lead_id={lead_id}")

    ultima_mensagem.status = dados.status
    db.commit()
    logger.info(f"Status atualizado: lead_id={lead_id} -> {dados.status}")
    return schemas.StatusResposta(lead_id=lead_id, status=dados.status)


# ============================================================
# POST /api/canais/{canal}/enviar
# Envia a resposta de volta ao canal de origem (chamado pelo
# node "Envia resposta ao canal" no n8n, depois do agente de IA
# gerar a resposta)
#
# IMPORTANTE: este endpoint hoje so registra a intencao de envio
# (log). A integracao real com a API do Facebook/Instagram (Meta
# Graph API) e do Google Ads precisa ser adicionada aqui depois -
# e um passo separado, com suas proprias credenciais/tokens.
# ============================================================
@app.post("/api/canais/{canal}/enviar")
def enviar_para_canal(canal: str, dados: schemas.EnviarCanal):
    logger.info(f"[ENVIO PENDENTE DE INTEGRACAO] canal={canal} lead_id={dados.lead_id} mensagem={dados.mensagem}")
    # TODO: chamar aqui a API real do canal (Meta Graph API para
    # Facebook/Instagram, Google Ads API, etc.), usando 'canal'
    # para decidir qual integracao usar.
    return {"status": "enviado_para_fila", "canal": canal, "lead_id": dados.lead_id}


@app.get("/")
def raiz():
    return {"status": "ok", "servico": "CRM IA - Backend de Leads"}
