# Diagrama do Esquema de Banco de Dados

## Diagrama Entidade-Relacionamento (ER)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INDE MCP - Database Schema                          │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────┐
│   t_classe_mapa         │
├─────────────────────────┤
│ PK id_classe_mapa       │◄─────┐
│    nome_classe_mapa     │      │
│    descricao            │      │
│    ativo                │      │
│    data_criacao         │      │
│    data_atualizacao     │      │
└─────────────────────────┘      │
                                 │
                                 │ FK id_classe_mapa
┌─────────────────────────┐      │
│   t_tipo_mapa           │      │
├─────────────────────────┤      │
│ PK id_tipo_mapa         │◄─────┼─────┐
│    nome_tipo_mapa       │      │     │
│    descricao            │      │     │
│    ativo                │      │     │
│    data_criacao         │      │     │
│    data_atualizacao     │      │     │
└─────────────────────────┘      │     │ FK id_tipo_mapa
                                 │     │
                                 │     │
┌─────────────────────────┐      │     │
│   t_anos                │      │     │
├─────────────────────────┤      │     │
│ PK id_ano               │◄─────┼─────┼─────┐
│    ano (UNIQUE)         │      │     │     │
│    descricao            │      │     │     │
│    ativo                │      │     │     │ FK id_ano
│    data_criacao         │      │     │     │
│    data_atualizacao     │      │     │     │
└─────────────────────────┘      │     │     │
                                 │     │     │
                                 │     │     │
┌──────────────────────────────────────────────────────────────┐
│   t_municipios                                               │
├──────────────────────────────────────────────────────────────┤
│ PK id_municipio (SERIAL)                                     │
│    cod_mun (UNIQUE) ───────────────────┐                     │
│    nom_mun                             │                     │
│    cod_uf                              │                     │
│    nom_uf                              │                     │
│    sigla_uf                            │                     │
│    regiao                              │                     │
│    populacao                           │                     │
│    area_km2                            │                     │
│    densidade_demografica (CALCULATED)  │                     │
│    capital                             │                     │
│    latitude                            │                     │
│    longitude                           │                     │
│    ativo                               │                     │
│    data_criacao                        │                     │
│    data_atualizacao                    │                     │
└────────────────────────────────────────┼─────────────────────┘
                                         │
                                         │ Relacionamento lógico
                                         │ (cod_mun)
                                         │
┌────────────────────────────────────────┼─────────────────────┐
│   t_publicacao_municipios              │                     │
├────────────────────────────────────────┼─────────────────────┤
│ PK id_publicacao_municipio (SERIAL)    │                     │
│    cod_mun ────────────────────────────┘                     │
│    nom_mun                                                   │
│ FK id_classe_mapa ──────────────────────────────────────────┘
│ FK id_tipo_mapa ────────────────────────────────────────────┘
│ FK id_ano ──────────────────────────────────────────────────┘
│    titulo_publicacao                                         │
│    descricao                                                 │
│    url_publicacao                                            │
│    escala                                                    │
│    datum                                                     │
│    sistema_projecao                                          │
│    formato_arquivo                                           │
│    tamanho_arquivo_mb                                        │
│    status (ATIVO|INATIVO|ARQUIVADO|EM_REVISAO)              │
│    data_publicacao                                           │
│    data_ultima_atualizacao                                   │
│    usuario_criacao                                           │
│    usuario_atualizacao                                       │
│    ativo                                                     │
│    data_criacao                                              │
│    data_modificacao                                          │
└──────────────────────────────────────────────────────────────┘

UNIQUE INDEX: (cod_mun, id_classe_mapa, id_tipo_mapa, id_ano)
```

## Relacionamentos

### 1. t_publicacao_municipios → t_classe_mapa
- **Tipo**: Many-to-One (N:1)
- **Cardinalidade**: Várias publicações podem ter a mesma classe de mapa
- **Constraint**: ON DELETE RESTRICT (não permite deletar classe se houver publicações)

### 2. t_publicacao_municipios → t_tipo_mapa
- **Tipo**: Many-to-One (N:1)
- **Cardinalidade**: Várias publicações podem ter o mesmo tipo de mapa
- **Constraint**: ON DELETE RESTRICT

### 3. t_publicacao_municipios → t_anos
- **Tipo**: Many-to-One (N:1)
- **Cardinalidade**: Várias publicações podem ter o mesmo ano
- **Constraint**: ON DELETE RESTRICT

### 4. t_publicacao_municipios ↔ t_municipios
- **Tipo**: Relacionamento lógico (não há FK física)
- **Cardinalidade**: Um município pode ter várias publicações
- **Ligação**: Através do campo `cod_mun` (código IBGE)
- **Nota**: Não há FK física para permitir flexibilidade na inserção de dados

## Índices Principais

### t_classe_mapa
- `PRIMARY KEY (id_classe_mapa)`
- `INDEX idx_classe_mapa_nome (nome_classe_mapa)`
- `INDEX idx_classe_mapa_ativo (ativo)`

### t_tipo_mapa
- `PRIMARY KEY (id_tipo_mapa)`
- `INDEX idx_tipo_mapa_nome (nome_tipo_mapa)`
- `INDEX idx_tipo_mapa_ativo (ativo)`

### t_anos
- `PRIMARY KEY (id_ano)`
- `UNIQUE INDEX (ano)`
- `INDEX idx_anos_ano (ano)`
- `INDEX idx_anos_ativo (ativo)`

### t_municipios
- `PRIMARY KEY (id_municipio)`
- `UNIQUE INDEX (cod_mun)`
- `INDEX idx_municipios_cod_mun (cod_mun)`
- `INDEX idx_municipios_nom_mun (nom_mun)`
- `INDEX idx_municipios_cod_uf (cod_uf)`
- `INDEX idx_municipios_sigla_uf (sigla_uf)`
- `INDEX idx_municipios_regiao (regiao)`
- `INDEX idx_municipios_capital (capital) WHERE capital = TRUE`
- `INDEX idx_municipios_uf_nome (sigla_uf, nom_mun)`
- `INDEX idx_municipios_coordenadas (latitude, longitude)`

### t_publicacao_municipios
- `PRIMARY KEY (id_publicacao_municipio)`
- `INDEX idx_t_publicacao_municipios_cod_mun (cod_mun)`
- `INDEX idx_t_publicacao_municipios_nom_mun (nom_mun)`
- `INDEX idx_t_publicacao_municipios_classe_tipo (id_classe_mapa, id_tipo_mapa)`
- `INDEX idx_t_publicacao_municipios_ano (id_ano)`
- `INDEX idx_t_publicacao_municipios_status (status)`
- `INDEX idx_t_publicacao_municipios_data_pub (data_publicacao)`
- `UNIQUE INDEX idx_t_publicacao_municipios_unique (cod_mun, id_classe_mapa, id_tipo_mapa, id_ano)`

## Triggers e Funções

### Funções Globais
1. **atualizar_data_modificacao()** - Atualiza automaticamente o campo de data de modificação
2. **calcular_densidade_demografica()** - Calcula densidade demográfica (população/área)
3. **atualizar_data_ultima_atualizacao()** - Atualiza data de última atualização

### Triggers em t_municipios
- `trigger_atualizar_municipios` - BEFORE UPDATE → atualizar_data_modificacao()
- `trigger_calcular_densidade` - BEFORE INSERT|UPDATE → calcular_densidade_demografica()

### Triggers em t_publicacao_municipios
- `trigger_atualizar_publicacao_municipios` - BEFORE UPDATE → atualizar_data_modificacao()
- `trigger_atualizar_data_ultima_atualizacao` - BEFORE UPDATE → atualizar_data_ultima_atualizacao()

### Funções Customizadas
- `obter_estatisticas_municipio(cod_mun VARCHAR)` - Retorna estatísticas de um município

## Views Principais

### Para t_municipios
1. `vw_municipios_resumo` - Resumo dos municípios ativos
2. `vw_capitais` - Lista de capitais brasileiras
3. `vw_municipios_por_regiao` - Estatísticas agregadas por região
4. `vw_municipios_por_uf` - Estatísticas agregadas por UF

### Para t_publicacao_municipios
1. `vw_t_publicacao_municipios_completa` - Dados completos com JOINs
2. `vw_resumo_publicacoes_municipio` - Estatísticas por município
3. `vw_publicacoes_por_ano` - Estatísticas por ano
4. `vw_publicacoes_por_classe` - Estatísticas por classe de mapa
5. `vw_publicacoes_recentes` - Publicações dos últimos 30 dias

## Fluxo de Dados

```
1. Cadastro de Município
   └─> t_municipios (cod_mun, nom_mun, dados geográficos)

2. Criação de Publicação
   ├─> Verificar t_classe_mapa (obter id_classe_mapa)
   ├─> Verificar t_tipo_mapa (obter id_tipo_mapa)
   ├─> Verificar t_anos (obter id_ano)
   └─> Inserir em t_publicacao_municipios
       └─> Validação de UNIQUE (cod_mun + classe + tipo + ano)

3. Consulta de Publicações
   └─> vw_t_publicacao_municipios_completa
       ├─> JOIN com t_classe_mapa
       ├─> JOIN com t_tipo_mapa
       └─> JOIN com t_anos
```

## Regras de Negócio

1. **Unicidade de Publicações**: Não pode haver duas publicações iguais (mesmo município, classe, tipo e ano)
2. **Integridade Referencial**: Não é possível deletar classes, tipos ou anos que tenham publicações
3. **Códigos IBGE**: Devem ter exatamente 7 dígitos
4. **Anos Válidos**: Entre 1900 e 2100
5. **Status de Publicação**: Apenas ATIVO, INATIVO, ARQUIVADO ou EM_REVISAO
6. **Densidade Demográfica**: Calculada automaticamente ao inserir/atualizar
7. **Coordenadas**: Latitude [-90, 90], Longitude [-180, 180]

## Considerações de Performance

- **Índices Compostos**: Otimizam consultas com múltiplos critérios
- **Índices Parciais**: Reduzem tamanho (ex: apenas capitais)
- **Views**: Abstraem complexidade mas podem impactar performance em grandes volumes
- **Triggers**: Executam automaticamente, considerar impacto em inserções em lote

## Extensões Futuras Recomendadas

1. **PostGIS**: Para consultas espaciais avançadas
2. **Geometrias**: Adicionar campos GEOMETRY para polígonos municipais
3. **Versionamento**: Tabela de histórico de alterações
4. **Cache**: Views materializadas para consultas pesadas
5. **Particionamento**: Por ano ou região para grandes volumes
6. **Full-Text Search**: Para busca de texto em descrições
