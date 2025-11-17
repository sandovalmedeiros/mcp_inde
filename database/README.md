# Estrutura de Banco de Dados - INDE MCP

Este diretório contém os schemas SQL para o banco de dados do sistema INDE MCP (Infraestrutura Nacional de Dados Espaciais - Model Context Protocol).

## 📊 Estrutura de Tabelas

### Tabelas de Referência

1. **t_classe_mapa** - Classificação dos mapas (base, temático, político, físico, cadastral)
2. **t_tipo_mapa** - Tipos de abrangência (municipal, estadual, regional, nacional, internacional)
3. **t_anos** - Anos de referência para publicações

### Tabelas Principais

4. **t_municipios** - Cadastro completo de municípios brasileiros (IBGE)
5. **t_publicacao_municipios** - Publicações de mapas por município

## 🔄 Ordem de Execução

Os scripts devem ser executados na seguinte ordem:

```bash
# 1. Criar tabelas de referência
psql -U seu_usuario -d seu_banco -f database/schemas/01_create_reference_tables.sql

# 2. Criar tabela de municípios
psql -U seu_usuario -d seu_banco -f database/schemas/02_create_municipios.sql

# 3. Criar tabela de publicações municipais
psql -U seu_usuario -d seu_banco -f database/schemas/03_create_publicacao_municipios.sql
```

Ou usar o script de execução automática:

```bash
bash database/create_database.sh
```

## 📋 Detalhamento das Tabelas

### 1. t_classe_mapa

Armazena as classificações de mapas disponíveis no sistema.

**Campos principais:**
- `id_classe_mapa` (VARCHAR(2)) - Chave primária
- `nome_classe_mapa` (VARCHAR(100)) - Nome da classe
- `descricao` (TEXT) - Descrição detalhada

**Dados pré-carregados:**
- 01 - Mapa Base
- 02 - Mapa Temático
- 03 - Mapa Político
- 04 - Mapa Físico
- 05 - Mapa Cadastral

### 2. t_tipo_mapa

Define os tipos de abrangência dos mapas.

**Campos principais:**
- `id_tipo_mapa` (VARCHAR(2)) - Chave primária
- `nome_tipo_mapa` (VARCHAR(100)) - Nome do tipo
- `descricao` (TEXT) - Descrição detalhada

**Dados pré-carregados:**
- 01 - Municipal
- 02 - Estadual
- 03 - Regional
- 04 - Nacional
- 05 - Internacional

### 3. t_anos

Gerencia os anos de referência para publicações.

**Campos principais:**
- `id_ano` (VARCHAR(2)) - Chave primária
- `ano` (INTEGER) - Ano (único, entre 1900 e 2100)
- `descricao` (VARCHAR(200)) - Descrição

**Dados pré-carregados:** Anos de 2015 a 2025 (id_ano: '01' a '11')

### 4. t_municipios

Cadastro completo de municípios brasileiros conforme IBGE.

**Campos principais:**
- `id_municipio` (SERIAL) - Chave primária
- `cod_mun` (VARCHAR(7)) - Código IBGE (único)
- `nom_mun` (VARCHAR(100)) - Nome do município
- `cod_uf` (VARCHAR(2)) - Código da UF
- `sigla_uf` (CHAR(2)) - Sigla da UF (SP, RJ, etc.)
- `regiao` (VARCHAR(20)) - Região geográfica
- `populacao` (INTEGER) - População estimada
- `area_km2` (NUMERIC(12,2)) - Área territorial
- `densidade_demografica` (NUMERIC(12,2)) - Calculada automaticamente
- `capital` (BOOLEAN) - Indica se é capital
- `latitude`, `longitude` (NUMERIC) - Coordenadas geográficas

**Triggers:**
- Atualização automática de `data_atualizacao`
- Cálculo automático de `densidade_demografica`

**Views disponíveis:**
- `vw_municipios_resumo` - Resumo de municípios ativos
- `vw_capitais` - Lista de capitais brasileiras
- `vw_municipios_por_regiao` - Estatísticas por região
- `vw_municipios_por_uf` - Estatísticas por UF

### 5. t_publicacao_municipios

Relaciona municípios com publicações de mapas georreferenciados.

**Campos principais:**
- `id_publicacao_municipio` (SERIAL) - Chave primária
- `cod_mun` (VARCHAR(7)) - Código IBGE do município
- `nom_mun` (VARCHAR(100)) - Nome do município
- `id_classe_mapa` (VARCHAR(2)) - FK para t_classe_mapa
- `id_tipo_mapa` (VARCHAR(2)) - FK para t_tipo_mapa
- `id_ano` (VARCHAR(2)) - FK para t_anos
- `titulo_publicacao` (VARCHAR(255)) - Título da publicação
- `url_publicacao` (VARCHAR(500)) - URL do arquivo
- `escala` (VARCHAR(50)) - Escala do mapa
- `datum` (VARCHAR(50)) - Sistema de referência (SIRGAS 2000, WGS84)
- `sistema_projecao` (VARCHAR(100)) - Sistema de projeção
- `formato_arquivo` (VARCHAR(50)) - Formato (GeoTIFF, Shapefile, etc.)
- `tamanho_arquivo_mb` (NUMERIC(10,2)) - Tamanho em MB
- `status` (VARCHAR(20)) - ATIVO, INATIVO, ARQUIVADO, EM_REVISAO

**Constraints:**
- Índice único: `(cod_mun, id_classe_mapa, id_tipo_mapa, id_ano)`
- Foreign keys com DELETE RESTRICT
- Check constraints para validação de dados

**Triggers:**
- Atualização automática de `data_modificacao`
- Atualização automática de `data_ultima_atualizacao`

**Views disponíveis:**
- `vw_t_publicacao_municipios_completa` - Dados completos com JOINs
- `vw_resumo_publicacoes_municipio` - Estatísticas por município
- `vw_publicacoes_por_ano` - Estatísticas por ano
- `vw_publicacoes_por_classe` - Estatísticas por classe de mapa
- `vw_publicacoes_recentes` - Publicações dos últimos 30 dias

**Funções utilitárias:**
- `obter_estatisticas_municipio(cod_mun)` - Estatísticas de um município específico

## 🔍 Exemplos de Consultas

### Listar todas as publicações de um município

```sql
SELECT * FROM vw_t_publicacao_municipios_completa
WHERE cod_mun = '3550308'; -- São Paulo
```

### Obter estatísticas de um município

```sql
SELECT * FROM obter_estatisticas_municipio('3550308');
```

### Publicações por região

```sql
SELECT
    mr.regiao,
    COUNT(pm.*) as total_publicacoes
FROM t_municipios m
LEFT JOIN t_publicacao_municipios pm ON m.cod_mun = pm.cod_mun
GROUP BY m.regiao;
```

### Publicações recentes

```sql
SELECT * FROM vw_publicacoes_recentes
ORDER BY data_publicacao DESC
LIMIT 10;
```

## 🔐 Segurança e Integridade

- **Foreign Keys**: Todas as referências usam `ON DELETE RESTRICT` para prevenir exclusões acidentais
- **Check Constraints**: Validação de dados em nível de banco
- **Unique Indexes**: Prevenção de duplicatas
- **Triggers**: Automação de cálculos e atualizações
- **Views**: Abstração de consultas complexas

## 📈 Performance

- **Índices estratégicos**: Criados para as consultas mais comuns
- **Índices compostos**: Para buscas multi-critério
- **Índices parciais**: Para filtros específicos (ex: capital = TRUE)
- **Views materializadas**: Podem ser criadas para consultas pesadas

## 🛠️ Manutenção

### Adicionar novos anos

```sql
INSERT INTO t_anos (id_ano, ano, descricao)
VALUES ('12', 2026, 'Ano base 2026');
```

### Adicionar nova classe de mapa

```sql
INSERT INTO t_classe_mapa (id_classe_mapa, nome_classe_mapa, descricao)
VALUES ('06', 'Mapa Hidrográfico', 'Mapas de recursos hídricos');
```

### Desativar publicação

```sql
UPDATE t_publicacao_municipios
SET status = 'INATIVO', ativo = FALSE
WHERE id_publicacao_municipio = 123;
```

## 📚 Referências

- [IBGE - Códigos de Municípios](https://www.ibge.gov.br/explica/codigos-dos-municipios.php)
- [INDE - Infraestrutura Nacional de Dados Espaciais](https://www.inde.gov.br/)
- [SIRGAS 2000](https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/sirgas.html)

## 💡 Próximos Passos

1. Popular `t_municipios` com dados do IBGE
2. Integrar com API do IBGE para atualização automática
3. Criar scripts de importação de publicações
4. Implementar versionamento de publicações
5. Adicionar suporte a geometrias (PostGIS)
6. Criar índices espaciais para consultas geográficas
