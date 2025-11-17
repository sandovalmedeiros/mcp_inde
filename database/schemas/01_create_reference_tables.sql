-- ============================================================
-- TABELAS DE REFERÊNCIA PARA O SISTEMA INDE
-- ============================================================
-- Descrição: Tabelas de suporte para classificação de mapas e anos
-- Autor: Sistema INDE MCP
-- Data: 2025-11-17
-- ============================================================

-- Tabela: t_classe_mapa
-- Descrição: Classificação dos mapas (ex: temático, base, referência)
CREATE TABLE t_classe_mapa (
    id_classe_mapa VARCHAR(2) PRIMARY KEY,
    nome_classe_mapa VARCHAR(100) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: t_tipo_mapa
-- Descrição: Tipos de mapas disponíveis (ex: político, físico, temático)
CREATE TABLE t_tipo_mapa (
    id_tipo_mapa VARCHAR(2) PRIMARY KEY,
    nome_tipo_mapa VARCHAR(100) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: t_anos
-- Descrição: Anos de referência para publicações
CREATE TABLE t_anos (
    id_ano VARCHAR(2) PRIMARY KEY,
    ano INTEGER NOT NULL UNIQUE,
    descricao VARCHAR(200),
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_ano_valido CHECK (ano >= 1900 AND ano <= 2100)
);

-- ============================================================
-- ÍNDICES PARA OTIMIZAÇÃO DE CONSULTAS
-- ============================================================

CREATE INDEX idx_classe_mapa_nome ON t_classe_mapa(nome_classe_mapa);
CREATE INDEX idx_classe_mapa_ativo ON t_classe_mapa(ativo);

CREATE INDEX idx_tipo_mapa_nome ON t_tipo_mapa(nome_tipo_mapa);
CREATE INDEX idx_tipo_mapa_ativo ON t_tipo_mapa(ativo);

CREATE INDEX idx_anos_ano ON t_anos(ano);
CREATE INDEX idx_anos_ativo ON t_anos(ativo);

-- ============================================================
-- DADOS INICIAIS (EXEMPLOS)
-- ============================================================

-- Classes de Mapa
INSERT INTO t_classe_mapa (id_classe_mapa, nome_classe_mapa, descricao) VALUES
('01', 'Mapa Base', 'Mapas de referência básica'),
('02', 'Mapa Temático', 'Mapas com informações específicas de um tema'),
('03', 'Mapa Político', 'Divisões político-administrativas'),
('04', 'Mapa Físico', 'Características físicas e geográficas'),
('05', 'Mapa Cadastral', 'Informações cadastrais e propriedades');

-- Tipos de Mapa
INSERT INTO t_tipo_mapa (id_tipo_mapa, nome_tipo_mapa, descricao) VALUES
('01', 'Municipal', 'Abrangência municipal'),
('02', 'Estadual', 'Abrangência estadual'),
('03', 'Regional', 'Abrangência regional'),
('04', 'Nacional', 'Abrangência nacional'),
('05', 'Internacional', 'Abrangência internacional');

-- Anos (últimos 10 anos como exemplo)
INSERT INTO t_anos (id_ano, ano, descricao) VALUES
('01', 2015, 'Ano base 2015'),
('02', 2016, 'Ano base 2016'),
('03', 2017, 'Ano base 2017'),
('04', 2018, 'Ano base 2018'),
('05', 2019, 'Ano base 2019'),
('06', 2020, 'Ano base 2020'),
('07', 2021, 'Ano base 2021'),
('08', 2022, 'Ano base 2022'),
('09', 2023, 'Ano base 2023'),
('10', 2024, 'Ano base 2024'),
('11', 2025, 'Ano base 2025');

-- ============================================================
-- COMENTÁRIOS NAS TABELAS
-- ============================================================

COMMENT ON TABLE t_classe_mapa IS 'Classificação dos tipos de mapas disponíveis no sistema INDE';
COMMENT ON TABLE t_tipo_mapa IS 'Tipos de abrangência dos mapas';
COMMENT ON TABLE t_anos IS 'Anos de referência para as publicações';
