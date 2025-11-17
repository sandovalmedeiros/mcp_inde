-- ============================================================
-- TABELA DE MUNICÍPIOS BRASILEIROS
-- ============================================================
-- Descrição: Cadastro completo de municípios do Brasil
-- Autor: Sistema INDE MCP
-- Data: 2025-11-17
-- ============================================================

-- Tabela: t_municipios
-- Descrição: Cadastro de municípios brasileiros conforme IBGE
CREATE TABLE t_municipios (
    -- Identificador único do município
    id_municipio SERIAL PRIMARY KEY,

    -- Código IBGE do município (7 dígitos)
    cod_mun VARCHAR(7) NOT NULL UNIQUE,

    -- Nome do município
    nom_mun VARCHAR(100) NOT NULL,

    -- Código da UF (2 dígitos)
    cod_uf VARCHAR(2) NOT NULL,

    -- Nome da UF
    nom_uf VARCHAR(50) NOT NULL,

    -- Sigla da UF
    sigla_uf CHAR(2) NOT NULL,

    -- Região geográfica
    regiao VARCHAR(20),

    -- População (última estimativa)
    populacao INTEGER,

    -- Área em km²
    area_km2 NUMERIC(12, 2),

    -- Densidade demográfica (hab/km²)
    densidade_demografica NUMERIC(12, 2),

    -- Capital (S/N)
    capital BOOLEAN DEFAULT FALSE,

    -- Dados geoespaciais
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),

    -- Metadados
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT chk_cod_mun_length CHECK (LENGTH(cod_mun) = 7),
    CONSTRAINT chk_cod_uf_length CHECK (LENGTH(cod_uf) = 2),
    CONSTRAINT chk_sigla_uf_length CHECK (LENGTH(sigla_uf) = 2),
    CONSTRAINT chk_populacao_positiva CHECK (populacao IS NULL OR populacao >= 0),
    CONSTRAINT chk_area_positiva CHECK (area_km2 IS NULL OR area_km2 > 0),
    CONSTRAINT chk_latitude_valida CHECK (latitude IS NULL OR (latitude >= -90 AND latitude <= 90)),
    CONSTRAINT chk_longitude_valida CHECK (longitude IS NULL OR (longitude >= -180 AND longitude <= 180))
);

-- ============================================================
-- ÍNDICES PARA OTIMIZAÇÃO DE CONSULTAS
-- ============================================================

-- Índice para busca por código IBGE
CREATE INDEX idx_municipios_cod_mun ON t_municipios(cod_mun);

-- Índice para busca por nome
CREATE INDEX idx_municipios_nom_mun ON t_municipios(nom_mun);

-- Índice para busca por UF
CREATE INDEX idx_municipios_cod_uf ON t_municipios(cod_uf);
CREATE INDEX idx_municipios_sigla_uf ON t_municipios(sigla_uf);

-- Índice para busca por região
CREATE INDEX idx_municipios_regiao ON t_municipios(regiao);

-- Índice para busca de capitais
CREATE INDEX idx_municipios_capital ON t_municipios(capital) WHERE capital = TRUE;

-- Índice para registros ativos
CREATE INDEX idx_municipios_ativo ON t_municipios(ativo);

-- Índice composto para consultas por UF e nome
CREATE INDEX idx_municipios_uf_nome ON t_municipios(sigla_uf, nom_mun);

-- Índice para coordenadas geográficas (útil para buscas espaciais)
CREATE INDEX idx_municipios_coordenadas ON t_municipios(latitude, longitude);

-- ============================================================
-- VIEWS ÚTEIS
-- ============================================================

-- View: Municípios com informações resumidas
CREATE VIEW vw_municipios_resumo AS
SELECT
    id_municipio,
    cod_mun,
    nom_mun,
    sigla_uf,
    nom_uf,
    regiao,
    capital,
    populacao,
    area_km2,
    densidade_demografica
FROM t_municipios
WHERE ativo = TRUE
ORDER BY nom_uf, nom_mun;

-- View: Capitais brasileiras
CREATE VIEW vw_capitais AS
SELECT
    id_municipio,
    cod_mun,
    nom_mun,
    sigla_uf,
    nom_uf,
    regiao,
    populacao,
    latitude,
    longitude
FROM t_municipios
WHERE capital = TRUE AND ativo = TRUE
ORDER BY nom_uf;

-- View: Municípios por região
CREATE VIEW vw_municipios_por_regiao AS
SELECT
    regiao,
    COUNT(*) as total_municipios,
    SUM(populacao) as populacao_total,
    SUM(area_km2) as area_total_km2,
    AVG(densidade_demografica) as densidade_media
FROM t_municipios
WHERE ativo = TRUE
GROUP BY regiao
ORDER BY regiao;

-- View: Municípios por UF
CREATE VIEW vw_municipios_por_uf AS
SELECT
    sigla_uf,
    nom_uf,
    regiao,
    COUNT(*) as total_municipios,
    SUM(populacao) as populacao_total,
    SUM(area_km2) as area_total_km2,
    AVG(densidade_demografica) as densidade_media
FROM t_municipios
WHERE ativo = TRUE
GROUP BY sigla_uf, nom_uf, regiao
ORDER BY sigla_uf;

-- ============================================================
-- COMENTÁRIOS NAS TABELAS E COLUNAS
-- ============================================================

COMMENT ON TABLE t_municipios IS 'Cadastro completo de municípios brasileiros conforme dados do IBGE';
COMMENT ON COLUMN t_municipios.cod_mun IS 'Código IBGE do município (7 dígitos)';
COMMENT ON COLUMN t_municipios.nom_mun IS 'Nome oficial do município';
COMMENT ON COLUMN t_municipios.cod_uf IS 'Código IBGE da Unidade Federativa';
COMMENT ON COLUMN t_municipios.sigla_uf IS 'Sigla da UF (ex: SP, RJ, MG)';
COMMENT ON COLUMN t_municipios.regiao IS 'Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)';
COMMENT ON COLUMN t_municipios.capital IS 'Indica se o município é capital estadual';
COMMENT ON COLUMN t_municipios.populacao IS 'População estimada do município';
COMMENT ON COLUMN t_municipios.area_km2 IS 'Área territorial em quilômetros quadrados';
COMMENT ON COLUMN t_municipios.densidade_demografica IS 'Densidade demográfica em habitantes por km²';

-- ============================================================
-- TRIGGERS PARA ATUALIZAÇÃO AUTOMÁTICA
-- ============================================================

-- Função para atualizar data_atualizacao automaticamente
CREATE OR REPLACE FUNCTION atualizar_data_modificacao()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para t_municipios
CREATE TRIGGER trigger_atualizar_municipios
    BEFORE UPDATE ON t_municipios
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_data_modificacao();

-- Função para calcular densidade demográfica automaticamente
CREATE OR REPLACE FUNCTION calcular_densidade_demografica()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.populacao IS NOT NULL AND NEW.area_km2 IS NOT NULL AND NEW.area_km2 > 0 THEN
        NEW.densidade_demografica = ROUND((NEW.populacao / NEW.area_km2)::NUMERIC, 2);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para calcular densidade automaticamente
CREATE TRIGGER trigger_calcular_densidade
    BEFORE INSERT OR UPDATE ON t_municipios
    FOR EACH ROW
    EXECUTE FUNCTION calcular_densidade_demografica();
