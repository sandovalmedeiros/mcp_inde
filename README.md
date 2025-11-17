# 🌐 INDE MCP - Interface Web para Dados Geoespaciais Brasileiros

[![Status](https://img.shields.io/badge/status-production-green)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

Interface web moderna e completa para interagir com o servidor MCP INDE (Infraestrutura Nacional de Dados Espaciais do Brasil).

---

## 📋 Conteúdo

- [Visão Geral](#-visão-geral)
- [Início Rápido](#-início-rápido)
- [Funcionalidades](#-funcionalidades)
- [Arquivos do Projeto](#-arquivos-do-projeto)
- [Documentação](#-documentação)
- [Como Usar](#-como-usar)
- [Ferramentas MCP](#-ferramentas-mcp)

---

## 🎯 Visão Geral

Este projeto fornece uma **interface web completa** para acessar dados geoespaciais de órgãos brasileiros através do **Model Context Protocol (MCP)**.

### O que você pode fazer:

- 🗺️ Acessar dados de **ANATEL, ANA, IBGE, INCRA, INPE** e outros
- 🔍 Descobrir serviços WFS, WMS e OWS disponíveis
- 💾 Extrair dados geoespaciais em GeoJSON e CSV
- 📊 Analisar capacidades completas de órgãos
- 🤖 Usar análise inteligente com agentes AI (CrewAI)
- 📄 Gerar relatórios automáticos

---

## 🚀 Início Rápido

### 1. Iniciar o Servidor

```bash
cd interface
python3 server.py
```

### 2. Acessar a Interface

Abra seu navegador em:
```
http://localhost:8000
```

### 3. Começar a Explorar!

Clique em **"Listar Serviços"** no menu e explore os dados geoespaciais brasileiros!

📖 **[Guia Completo de Início Rápido →](QUICKSTART.md)**

---

## ✨ Funcionalidades

### Interface Web

- ✅ **Dashboard intuitivo** com visão geral do sistema
- ✅ **6 ferramentas MCP integradas** com formulários interativos
- ✅ **Visualização de resultados** em tabelas, cards e gráficos
- ✅ **Design responsivo** funciona em desktop e mobile
- ✅ **Modo demonstração** com dados simulados para testes
- ✅ **Servidor HTTP embutido** - sem dependências externas

### Servidor MCP

- ✅ **Extração automática** de dados WFS/WMS/OWS
- ✅ **Descoberta de camadas** automática
- ✅ **Análise inteligente** com agentes AI (CrewAI)
- ✅ **Geração de relatórios** em múltiplos formatos
- ✅ **Cache de serviços** para performance
- ✅ **Tratamento de erros** robusto

---

## 📁 Arquivos do Projeto

### Interface Web (Diretório `interface/`)

```
interface/
├── index.html          # Interface principal (16KB)
├── styles.css          # Estilos CSS modernos (11KB)
├── app.js              # Lógica JavaScript (29KB)
└── server.py           # Servidor HTTP (2.7KB)
```

### Servidor MCP e Configuração

```
mcp_inde/
├── mcp_inde_server_main.py    # Servidor MCP principal
├── monitoring_system.py        # Sistema de monitoramento
├── catalogo_inde.yaml         # Catálogo de serviços INDE
├── catalogo_servicos_inde.json # Catálogo em JSON
└── mcp_config.json            # Configuração MCP
```

### Documentação

```
├── README.md                  # Este arquivo
├── INTERFACE_README.md        # Documentação completa da interface
├── QUICKSTART.md              # Guia de início rápido
├── complete_guide_mcp.md      # Guia completo MCP
└── manual_usuario.md          # Manual do usuário
```

---

## 📚 Documentação

| Documento | Descrição | Tamanho |
|-----------|-----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | Comece a usar em 3 minutos | 4.6KB |
| **[INTERFACE_README.md](INTERFACE_README.md)** | Documentação completa da interface | 13KB |
| **[complete_guide_mcp.md](complete_guide_mcp.md)** | Guia completo do servidor MCP | 20KB |
| **[manual_usuario.md](manual_usuario.md)** | Manual do usuário final | 8.1KB |

---

## 💻 Como Usar

### Opção 1: Interface Web (Recomendado)

**Melhor para:** Usuários que preferem interface gráfica

```bash
# 1. Iniciar servidor
cd interface
python3 server.py

# 2. Abrir navegador
# Acesse: http://localhost:8000

# 3. Explorar dados através da interface
```

### Opção 2: Claude Desktop (Avançado)

**Melhor para:** Integração com Claude AI

1. Edite a configuração do Claude Desktop
2. Adicione o conteúdo de `mcp_config.json`
3. Reinicie o Claude Desktop
4. Use comandos naturais no Claude

**Exemplo:**
```
"Liste os serviços geoespaciais da ANATEL"
"Extraia dados da camada de municípios do IBGE"
```

📖 **[Ver instruções detalhadas →](INTERFACE_README.md#-configuração-com-claude-desktop)**

### Opção 3: Servidor MCP Standalone

**Melhor para:** Desenvolvimento e integração

```bash
# Executar servidor MCP diretamente
python3 mcp_inde_server_main.py
```

---

## 🛠️ Ferramentas MCP

### 1. `list_inde_services`
Lista todos os serviços geoespaciais disponíveis na INDE.

**Uso:**
```python
list_inde_services(orgao="ANATEL")
```

### 2. `discover_service_layers`
Descobre camadas disponíveis em um serviço.

**Uso:**
```python
discover_service_layers(
    orgao="ANATEL",
    service_name="telecomunicações"
)
```

### 3. `extract_geospatial_data`
Extrai dados de uma camada específica.

**Uso:**
```python
extract_geospatial_data(
    orgao="ANATEL",
    service_name="telecomunicações",
    layer="anatel:estacoes",
    max_features=1000
)
```

### 4. `analyze_organization_capabilities`
Analisa capacidades completas de um órgão.

**Uso:**
```python
analyze_organization_capabilities(orgao="ANATEL")
```

### 5. `intelligent_data_analysis`
Executa análise inteligente com agentes AI.

**Uso:**
```python
intelligent_data_analysis(
    orgao="ANATEL",
    objetivo="Analisar infraestrutura de telecomunicações"
)
```

### 6. `generate_data_report`
Gera relatório automático.

**Uso:**
```python
generate_data_report(
    orgao="ANATEL",
    format="markdown"
)
```

---

## 🏢 Órgãos Disponíveis

A interface dá acesso a dados de diversos órgãos brasileiros:

| Órgão | Nome Completo | Tipos |
|-------|---------------|-------|
| **ANATEL** | Agência Nacional de Telecomunicações | WFS, WMS, OWS |
| **ANA** | Agência Nacional de Águas | WMS |
| **IBGE** | Instituto Brasileiro de Geografia e Estatística | WFS, WMS |
| **INCRA** | Instituto Nacional de Colonização e Reforma Agrária | OWS |
| **INPE** | Instituto Nacional de Pesquisas Espaciais | WMS |
| **DNIT** | Departamento Nacional de Infraestrutura de Transportes | OWS |
| **ICMBio** | Instituto Chico Mendes de Conservação da Biodiversidade | WFS |
| **ANM** | Agência Nacional de Mineração | OWS |
| **ANP** | Agência Nacional do Petróleo | OWS |

E muitos outros...

---

## 🔧 Requisitos

### Software

- Python 3.8 ou superior
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Dependências Python

```bash
pip install fastmcp pydantic crewai requests pyyaml pandas
```

---

## 📦 Instalação

### Clone ou baixe o repositório

```bash
cd /home/user/mcp_inde
```

### Instale as dependências

```bash
pip install fastmcp pydantic crewai requests pyyaml pandas
```

### Execute o servidor da interface

```bash
cd interface
python3 server.py
```

### Acesse no navegador

```
http://localhost:8000
```

---

## 🎨 Screenshots

### Dashboard
Interface principal com visão geral das funcionalidades

### Listar Serviços
Visualização de todos os serviços geoespaciais disponíveis

### Extrair Dados
Formulário interativo para extração de dados com estatísticas

### Gerar Relatório
Relatórios automáticos em Markdown, JSON ou HTML

---

## 🔍 Solução de Problemas

### Porta ocupada?

```bash
python3 server.py 8080  # Use outra porta
```

### Módulos não encontrados?

```bash
pip install fastmcp pydantic crewai requests pyyaml pandas
```

### Interface não carrega?

1. Verifique se o servidor está rodando
2. Acesse `http://localhost:8000` (não `file:///...`)
3. Limpe o cache do navegador

📖 **[Ver guia completo de solução de problemas →](INTERFACE_README.md#-solução-de-problemas)**

---

## 📊 Arquitetura

```
┌─────────────────────┐
│   Interface Web     │  ← Você está aqui
│  (HTML/CSS/JS)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Servidor MCP      │
│   (FastMCP)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Serviços INDE      │
│  (WFS/WMS/OWS)      │
└─────────────────────┘
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é fornecido como está, para uso educacional e de pesquisa.

---

## 🙏 Agradecimentos

- **INDE** - Infraestrutura Nacional de Dados Espaciais
- **Órgãos Brasileiros** - Por disponibilizarem dados abertos
- **FastMCP** - Framework MCP para Python
- **CrewAI** - Framework para agentes AI
- **Comunidade Open Source** - Por ferramentas e bibliotecas incríveis

---

## 📞 Suporte

Para dúvidas e problemas:

1. Consulte **[QUICKSTART.md](QUICKSTART.md)** para início rápido
2. Leia **[INTERFACE_README.md](INTERFACE_README.md)** para documentação completa
3. Verifique a seção de solução de problemas

---

## 🗺️ Roadmap

### v1.0 (Atual) ✅
- Interface web completa
- 6 ferramentas MCP
- Modo demonstração
- Documentação completa

### v1.1 (Próximo)
- Integração real com servidor MCP via WebSocket
- Visualização de mapas com Leaflet
- Cache de resultados
- Histórico de consultas

### v2.0 (Futuro)
- Análise espacial avançada
- Exportação para múltiplos formatos
- Dashboard de monitoramento
- API REST

---

**Desenvolvido com ❤️ para facilitar o acesso a dados geoespaciais brasileiros**

🇧🇷 **Brasil** | 🗺️ **Dados Abertos** | 🚀 **Tecnologia**
