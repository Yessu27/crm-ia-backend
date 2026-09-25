-- ============================================================
-- Schema da tabela de mensagens/leads do CRM
-- Rode este script no seu Postgres (local, Supabase, ou RDS na AWS)
-- ============================================================

CREATE TABLE IF NOT EXISTS mensagens (
    id              SERIAL PRIMARY KEY,
    lead_id         VARCHAR(100) NOT NULL,
    canal_origem    VARCHAR(50)  NOT NULL,   -- 'facebook', 'instagram', 'google_ads'
    mensagem        TEXT         NOT NULL,
    status          VARCHAR(50)  NOT NULL DEFAULT 'aguardando_resposta',
                    -- valores possíveis: aguardando_resposta | respondido_por_humano | respondido_por_ia
    timestamp       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Índice para consultas rápidas de status por lead (usado pelo n8n a cada 5 min)
CREATE INDEX IF NOT EXISTS idx_mensagens_lead_id ON mensagens (lead_id);
CREATE INDEX IF NOT EXISTS idx_mensagens_status ON mensagens (status);
