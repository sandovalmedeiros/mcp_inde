-- ============================================================
-- TABELA DE PUBLICAÇÕES MUNICIPAIS
-- ============================================================
-- Descrição: Relacionamento entre municípios e publicações de mapas
-- Autor: Sistema INDE MCP
-- Data: 2025-11-17
-- ============================================================

-- Tabela: t_publicacao_municipios
-- Descrição: Registro de publicações de mapas por município
CREATE TABLE t_publicacao_municipios (
    -- Identificador principal
    id_publicacao_municipio SERIAL PRIMARY KEY,

    -- Dados do município
    cod_mun VARCHAR(7) NOT NULL,
    nom_mun VARCHAR(100) NOT NULL,

    -- Chaves estrangeiras para classificação
    id_classe_mapa VARCHAR(2) NOT NULL,
    id_tipo_mapa VARCHAR(2) NOT NULL,
    id_ano VARCHAR(2) NOT NULL,

    -- Metadados adicionais
    titulo_publicacao VARCHAR(255),
    descricao TEXT,
    url_publicacao VARCHAR(500),
    escala VARCHAR(50),
    datum VARCHAR(50),
    sistema_projecao VARCHAR(100),
    formato_arquivo VARCHAR(50),
    tamanho_arquivo_mb NUMERIC(10, 2),

    -- Status da publicação
    status VARCHAR(20) DEFAULT 'ATIVO' CHECK (status IN ('ATIVO', 'INATIVO', 'ARQUIVADO', 'EM_REVISAO')),

    -- Dados de auditoria
    data_publicacao DATE,
    data_ultima_atualizacao DATE,
    usuario_criacao VARCHAR(100),
    usuario_atualizacao VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Keys para integridade referencial
    CONSTRAINT fk_t_pub_municipios_classe_mapa
        FOREIGN KEY (id_classe_mapa)
        REFERENCES t_classe_mapa(id_classe_mapa)
        ON DELETE RESTRICT,

    CONSTRAINT fk_t_pub_municipios_tipo_mapa
        FOREIGN KEY (id_tipo_mapa)
        REFERENCES t_tipo_mapa(id_tipo_mapa)
        ON DELETE RESTRICT,

    CONSTRAINT fk_t_pub_municipios_ano
        FOREIGN KEY (id_ano)
        REFERENCES t_anos(id_ano)
        ON DELETE RESTRICT,

    -- Validações
    CONSTRAINT chk_cod_mun_length CHECK (LENGTH(cod_mun) = 7),
    CONSTRAINT chk_tamanho_arquivo CHECK (tamanho_arquivo_mb IS NULL OR tamanho_arquivo_mb > 0)
);

-- ============================================================
-- ÍNDICES PARA OTIMIZAÇÃO DE CONSULTAS
-- ============================================================

-- Índice para busca por código do município
CREATE INDEX idx_t_publicacao_municipios_cod_mun
    ON t_publicacao_municipios(cod_mun);

-- Índice para busca por nome do município
CREATE INDEX idx_t_publicacao_municipios_nom_mun
    ON t_publicacao_municipios(nom_mun);

-- Índice composto para busca por classe e tipo de mapa
CREATE INDEX idx_t_publicacao_municipios_classe_tipo
    ON t_publicacao_municipios(id_classe_mapa, id_tipo_mapa);

-- Índice para busca por ano
CREATE INDEX idx_t_publicacao_municipios_ano
    ON t_publicacao_municipios(id_ano);

-- Índice para busca por status
CREATE INDEX idx_t_publicacao_municipios_status
    ON t_publicacao_municipios(status);

-- Índice para busca por data de publicação
CREATE INDEX idx_t_publicacao_municipios_data_pub
    ON t_publicacao_municipios(data_publicacao);

-- Índice para registros ativos
CREATE INDEX idx_t_publicacao_municipios_ativo
    ON t_publicacao_municipios(ativo) WHERE ativo = TRUE;

-- Índice único para evitar duplicatas
CREATE UNIQUE INDEX idx_t_publicacao_municipios_unique
    ON t_publicacao_municipios(cod_mun, id_classe_mapa, id_tipo_mapa, id_ano);

-- ============================================================
-- VIEWS PARA CONSULTAS FACILITADAS
-- ============================================================

-- View: Publicações municipais completas
CREATE VIEW vw_t_publicacao_municipios_completa AS
SELECT
    pm.id_publicacao_municipio,
    pm.cod_mun,
    pm.nom_mun,

    -- Classificação principal
    cm.id_classe_mapa,
    cm.nome_classe_mapa,
    cm.descricao AS descricao_classe,

    -- Tipo de mapa
    tm.id_tipo_mapa,
    tm.nome_tipo_mapa,
    tm.descricao AS descricao_tipo,

    -- Ano
    a.id_ano,
    a.ano,

    -- Dados da publicação
    pm.titulo_publicacao,
    pm.descricao,
    pm.url_publicacao,
    pm.escala,
    pm.datum,
    pm.sistema_projecao,
    pm.formato_arquivo,
    pm.tamanho_arquivo_mb,
    pm.status,
    pm.data_publicacao,
    pm.data_ultima_atualizacao,
    pm.usuario_criacao,
    pm.usuario_atualizacao,
    pm.ativo
FROM t_publicacao_municipios pm
JOIN t_classe_mapa cm ON pm.id_classe_mapa = cm.id_classe_mapa
JOIN t_tipo_mapa tm ON pm.id_tipo_mapa = tm.id_tipo_mapa
JOIN t_anos a ON pm.id_ano = a.id_ano
WHERE pm.ativo = TRUE
ORDER BY pm.data_publicacao DESC;

-- View: Resumo de publicações por município
CREATE VIEW vw_resumo_publicacoes_municipio AS
SELECT
    cod_mun,
    nom_mun,
    COUNT(*) as total_publicacoes,
    COUNT(DISTINCT id_classe_mapa) as total_classes,
    COUNT(DISTINCT id_tipo_mapa) as total_tipos,
    COUNT(DISTINCT id_ano) as total_anos,
    MAX(data_publicacao) as ultima_publicacao,
    SUM(tamanho_arquivo_mb) as tamanho_total_mb
FROM t_publicacao_municipios
WHERE ativo = TRUE AND status = 'ATIVO'
GROUP BY cod_mun, nom_mun
ORDER BY total_publicacoes DESC;

-- View: Publicações por ano
CREATE VIEW vw_publicacoes_por_ano AS
SELECT
    a.ano,
    COUNT(*) as total_publicacoes,
    COUNT(DISTINCT pm.cod_mun) as total_municipios,
    COUNT(DISTINCT pm.id_classe_mapa) as total_classes,
    COUNT(DISTINCT pm.id_tipo_mapa) as total_tipos,
    SUM(pm.tamanho_arquivo_mb) as tamanho_total_mb
FROM t_publicacao_municipios pm
JOIN t_anos a ON pm.id_ano = a.id_ano
WHERE pm.ativo = TRUE AND pm.status = 'ATIVO'
GROUP BY a.ano
ORDER BY a.ano DESC;

-- View: Publicações por classe de mapa
CREATE VIEW vw_publicacoes_por_classe AS
SELECT
    cm.id_classe_mapa,
    cm.nome_classe_mapa,
    COUNT(*) as total_publicacoes,
    COUNT(DISTINCT pm.cod_mun) as total_municipios,
    COUNT(DISTINCT pm.id_ano) as total_anos,
    AVG(pm.tamanho_arquivo_mb) as tamanho_medio_mb
FROM t_publicacao_municipios pm
JOIN t_classe_mapa cm ON pm.id_classe_mapa = cm.id_classe_mapa
WHERE pm.ativo = TRUE AND pm.status = 'ATIVO'
GROUP BY cm.id_classe_mapa, cm.nome_classe_mapa
ORDER BY total_publicacoes DESC;

-- View: Publicações recentes (últimos 30 dias)
CREATE VIEW vw_publicacoes_recentes AS
SELECT
    pm.id_publicacao_municipio,
    pm.cod_mun,
    pm.nom_mun,
    cm.nome_classe_mapa,
    tm.nome_tipo_mapa,
    a.ano,
    pm.titulo_publicacao,
    pm.data_publicacao,
    pm.tamanho_arquivo_mb,
    pm.status
FROM t_publicacao_municipios pm
JOIN t_classe_mapa cm ON pm.id_classe_mapa = cm.id_classe_mapa
JOIN t_tipo_mapa tm ON pm.id_tipo_mapa = tm.id_tipo_mapa
JOIN t_anos a ON pm.id_ano = a.id_ano
WHERE pm.ativo = TRUE
    AND pm.data_publicacao >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY pm.data_publicacao DESC;

-- ============================================================
-- TRIGGERS PARA AUTOMAÇÃO
-- ============================================================

-- Trigger para atualizar data_modificacao automaticamente
CREATE TRIGGER trigger_atualizar_publicacao_municipios
    BEFORE UPDATE ON t_publicacao_municipios
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_data_modificacao();

-- Função para atualizar data_ultima_atualizacao
CREATE OR REPLACE FUNCTION atualizar_data_ultima_atualizacao()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_ultima_atualizacao = CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para atualizar data_ultima_atualizacao
CREATE TRIGGER trigger_atualizar_data_ultima_atualizacao
    BEFORE UPDATE ON t_publicacao_municipios
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION atualizar_data_ultima_atualizacao();

-- ============================================================
-- COMENTÁRIOS NAS TABELAS
-- ============================================================

COMMENT ON TABLE t_publicacao_municipios IS 'Registro de publicações de mapas georreferenciados por município';
COMMENT ON COLUMN t_publicacao_municipios.cod_mun IS 'Código IBGE do município (7 dígitos)';
COMMENT ON COLUMN t_publicacao_municipios.nom_mun IS 'Nome do município';
COMMENT ON COLUMN t_publicacao_municipios.id_classe_mapa IS 'Referência para a classe do mapa';
COMMENT ON COLUMN t_publicacao_municipios.id_tipo_mapa IS 'Referência para o tipo de mapa';
COMMENT ON COLUMN t_publicacao_municipios.id_ano IS 'Referência para o ano da publicação';
COMMENT ON COLUMN t_publicacao_municipios.titulo_publicacao IS 'Título ou nome da publicação';
COMMENT ON COLUMN t_publicacao_municipios.escala IS 'Escala do mapa (ex: 1:50.000)';
COMMENT ON COLUMN t_publicacao_municipios.datum IS 'Sistema de referência geodésico (ex: SIRGAS 2000, WGS84)';
COMMENT ON COLUMN t_publicacao_municipios.sistema_projecao IS 'Sistema de projeção cartográfica utilizado';
COMMENT ON COLUMN t_publicacao_municipios.status IS 'Status atual da publicação (ATIVO, INATIVO, ARQUIVADO, EM_REVISAO)';

-- ============================================================
-- FUNÇÕES UTILITÁRIAS
-- ============================================================

-- Função para obter estatísticas de um município específico
CREATE OR REPLACE FUNCTION obter_estatisticas_municipio(p_cod_mun VARCHAR)
RETURNS TABLE (
    codigo_municipio VARCHAR,
    nome_municipio VARCHAR,
    total_publicacoes BIGINT,
    total_classes BIGINT,
    total_tipos BIGINT,
    total_anos BIGINT,
    primeira_publicacao DATE,
    ultima_publicacao DATE,
    tamanho_total_mb NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        pm.cod_mun,
        pm.nom_mun,
        COUNT(*)::BIGINT,
        COUNT(DISTINCT pm.id_classe_mapa)::BIGINT,
        COUNT(DISTINCT pm.id_tipo_mapa)::BIGINT,
        COUNT(DISTINCT pm.id_ano)::BIGINT,
        MIN(pm.data_publicacao),
        MAX(pm.data_publicacao),
        SUM(pm.tamanho_arquivo_mb)
    FROM t_publicacao_municipios pm
    WHERE pm.cod_mun = p_cod_mun
        AND pm.ativo = TRUE
        AND pm.status = 'ATIVO'
    GROUP BY pm.cod_mun, pm.nom_mun;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION obter_estatisticas_municipio IS 'Retorna estatísticas resumidas de publicações para um município específico';
