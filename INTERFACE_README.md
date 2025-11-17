# 🌐 Interface Web - INDE MCP

Interface web moderna e interativa para usar o servidor MCP INDE (Infraestrutura Nacional de Dados Espaciais).

![Status](https://img.shields.io/badge/status-production-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📑 Índice

1. [Visão Geral](#-visão-geral)
2. [Funcionalidades](#-funcionalidades)
3. [Instalação](#-instalação)
4. [Uso](#-uso)
5. [Configuração com Claude Desktop](#-configuração-com-claude-desktop)
6. [Ferramentas MCP Disponíveis](#-ferramentas-mcp-disponíveis)
7. [Arquitetura](#-arquitetura)
8. [Solução de Problemas](#-solução-de-problemas)

---

## 🎯 Visão Geral

Esta interface web permite interagir facilmente com o servidor MCP INDE através de uma interface gráfica moderna, sem necessidade de conhecimento em linha de comando ou programação.

### O que é possível fazer:

- 📊 **Listar serviços** geoespaciais de órgãos brasileiros (ANATEL, ANA, IBGE, etc.)
- 🔍 **Descobrir camadas** disponíveis em cada serviço
- 💾 **Extrair dados** de camadas específicas em formatos GeoJSON e CSV
- 📈 **Analisar capacidades** completas de um órgão
- 🤖 **Análise inteligente** usando agentes AI (CrewAI)
- 📄 **Gerar relatórios** automáticos em Markdown, JSON ou HTML

---

## ✨ Funcionalidades

### 1. Dashboard Intuitivo
- Visão geral das capacidades do sistema
- Acesso rápido a todas as ferramentas
- Guia de início rápido

### 2. Navegação por Abas
- Interface organizada por funcionalidade
- Navegação fluida entre seções
- Design responsivo para desktop e mobile

### 3. Visualização de Resultados
- Estatísticas em cards visuais
- Tabelas interativas de dados
- Formatação JSON elegante
- Download de relatórios

### 4. Modo Demonstração
- Funciona standalone sem conexão ao servidor
- Dados simulados para teste
- Útil para entender o fluxo de trabalho

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Passo 1: Estrutura de Arquivos

Certifique-se de ter a seguinte estrutura:

```
mcp_inde/
├── interface/
│   ├── index.html          # Interface principal
│   ├── styles.css          # Estilos CSS
│   ├── app.js              # Lógica JavaScript
│   └── server.py           # Servidor HTTP
├── mcp_inde_server_main.py # Servidor MCP
├── catalogo_inde.yaml      # Catálogo de serviços
├── mcp_config.json         # Configuração MCP
└── INTERFACE_README.md     # Esta documentação
```

### Passo 2: Instalar Dependências

```bash
# Navegar para o diretório do projeto
cd /home/user/mcp_inde

# Instalar dependências Python (se ainda não instalou)
pip install fastmcp pydantic crewai requests pyyaml pandas
```

### Passo 3: Tornar o servidor executável

```bash
chmod +x interface/server.py
```

---

## 💻 Uso

### Método 1: Usando Python

```bash
# A partir do diretório mcp_inde
cd interface
python3 server.py

# Ou especifique uma porta diferente
python3 server.py 8080
```

### Método 2: Servidor HTTP Built-in do Python

```bash
cd interface
python3 -m http.server 8000
```

### Acessando a Interface

1. Inicie o servidor usando um dos métodos acima
2. Abra seu navegador
3. Acesse: `http://localhost:8000` (ou a porta que você escolheu)
4. Comece a explorar os dados geoespaciais!

---

## 🔧 Configuração com Claude Desktop

Para usar o servidor MCP diretamente com o Claude Desktop (aplicação oficial):

### Passo 1: Localizar o arquivo de configuração

**No macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**No Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**No Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Passo 2: Adicionar a configuração

Abra o arquivo e adicione a configuração do servidor INDE MCP:

```json
{
  "mcpServers": {
    "inde-geospatial": {
      "command": "python3",
      "args": [
        "/caminho/absoluto/para/mcp_inde/mcp_inde_server_main.py"
      ],
      "env": {
        "PYTHONPATH": "/caminho/absoluto/para/mcp_inde",
        "CATALOG_PATH": "/caminho/absoluto/para/mcp_inde/catalogo_inde.yaml"
      }
    }
  }
}
```

**⚠️ IMPORTANTE:** Substitua `/caminho/absoluto/para/` pelo caminho real do seu sistema!

### Passo 3: Reiniciar Claude Desktop

1. Feche completamente o Claude Desktop
2. Abra novamente
3. O servidor MCP INDE estará disponível

### Passo 4: Usar no Claude

Agora você pode fazer perguntas ao Claude como:

```
"Liste os serviços geoespaciais da ANATEL"
"Descubra as camadas disponíveis no serviço WFS do IBGE"
"Extraia dados da camada de municípios do INCRA"
"Gere um relatório sobre os dados disponíveis da ANA"
```

---

## 🛠️ Ferramentas MCP Disponíveis

### 1. `list_inde_services`

Lista todos os serviços geoespaciais disponíveis na INDE.

**Parâmetros:**
- `orgao` (opcional): Filtrar por órgão específico

**Exemplo de uso:**
```python
# Listar todos os serviços
list_inde_services()

# Filtrar por órgão
list_inde_services(orgao="ANATEL")
```

---

### 2. `discover_service_layers`

Descobre camadas disponíveis em um serviço específico.

**Parâmetros:**
- `orgao` (obrigatório): Nome do órgão (ex: ANATEL, ANA, IBGE)
- `service_name` (obrigatório): Nome ou parte do nome do serviço

**Exemplo de uso:**
```python
discover_service_layers(
    orgao="ANATEL",
    service_name="telecomunicações"
)
```

---

### 3. `extract_geospatial_data`

Extrai dados de uma camada geoespacial específica.

**Parâmetros:**
- `orgao` (obrigatório): Nome do órgão
- `service_name` (obrigatório): Nome do serviço
- `layer` (obrigatório): Nome da camada
- `max_features` (opcional): Número máximo de registros (padrão: 1000)

**Exemplo de uso:**
```python
extract_geospatial_data(
    orgao="ANATEL",
    service_name="telecomunicações",
    layer="anatel:estacoes",
    max_features=1000
)
```

---

### 4. `analyze_organization_capabilities`

Analisa todas as capacidades de dados de um órgão.

**Parâmetros:**
- `orgao` (obrigatório): Nome do órgão para análise

**Exemplo de uso:**
```python
analyze_organization_capabilities(orgao="ANATEL")
```

---

### 5. `intelligent_data_analysis`

Executa análise inteligente usando agentes AI (CrewAI).

**Parâmetros:**
- `orgao` (obrigatório): Nome do órgão
- `objetivo` (obrigatório): Objetivo da análise

**Exemplo de uso:**
```python
intelligent_data_analysis(
    orgao="ANATEL",
    objetivo="Analisar infraestrutura de telecomunicações no Brasil"
)
```

**⚠️ Nota:** Esta funcionalidade pode levar alguns minutos para completar.

---

### 6. `generate_data_report`

Gera relatório automático sobre os dados disponíveis de um órgão.

**Parâmetros:**
- `orgao` (obrigatório): Nome do órgão
- `format` (opcional): Formato do relatório (markdown, json, html) - padrão: markdown

**Exemplo de uso:**
```python
generate_data_report(
    orgao="ANATEL",
    format="markdown"
)
```

---

## 🏗️ Arquitetura

### Componentes

```
┌─────────────────────┐
│   Interface Web     │
│  (HTML/CSS/JS)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Servidor HTTP     │
│   (Python)          │
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
│  Extrator INDE      │
│  (WFS/WMS/OWS)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Agentes CrewAI     │
│  (Análise AI)       │
└─────────────────────┘
```

### Fluxo de Dados

1. **Interface Web** → Usuário interage com formulários
2. **JavaScript** → Processa requisições e valida dados
3. **Servidor HTTP** → Serve arquivos estáticos
4. **Servidor MCP** → Executa ferramentas e retorna resultados
5. **Extrator INDE** → Conecta com serviços geoespaciais
6. **Agentes AI** → Realiza análises inteligentes (quando solicitado)
7. **Interface** → Exibe resultados formatados

---

## 🔍 Solução de Problemas

### Problema: Porta já está em uso

**Erro:**
```
OSError: [Errno 98] Address already in use
```

**Solução:**
```bash
# Use uma porta diferente
python3 server.py 8080

# Ou encontre e mate o processo usando a porta
lsof -ti:8000 | xargs kill -9
```

---

### Problema: Módulos Python não encontrados

**Erro:**
```
ModuleNotFoundError: No module named 'fastmcp'
```

**Solução:**
```bash
# Instalar dependências
pip install fastmcp pydantic crewai requests pyyaml pandas

# Ou usar requirements.txt (se disponível)
pip install -r requirements.txt
```

---

### Problema: Interface não carrega estilos

**Solução:**

1. Verifique que todos os arquivos estão no diretório correto:
   ```bash
   ls -la interface/
   # Deve mostrar: index.html, styles.css, app.js, server.py
   ```

2. Limpe o cache do navegador:
   - Chrome: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Safari: Cmd+Option+E

3. Certifique-se de estar acessando `http://localhost:8000` e não `file:///...`

---

### Problema: Servidor MCP não responde

**Sintomas:**
- Interface carrega mas mostra "Desconectado"
- Operações retornam erro

**Solução:**

1. Verifique se o servidor MCP está rodando:
   ```bash
   python3 mcp_inde_server_main.py
   ```

2. Verifique o arquivo de configuração (`mcp_config.json`)

3. Teste individualmente as ferramentas MCP

---

### Problema: Dados não carregam

**Possíveis causas:**

1. **Serviço INDE offline** → Tente outro órgão/serviço
2. **Timeout de rede** → Reduza `max_features` para 100-500
3. **Camada inválida** → Use `discover_service_layers` para ver camadas válidas
4. **Filtros incorretos** → Verifique ortografia do nome do órgão

---

## 📊 Órgãos Disponíveis

A interface dá acesso a serviços geoespaciais de diversos órgãos brasileiros:

- **ANATEL** - Agência Nacional de Telecomunicações
- **ANA** - Agência Nacional de Águas e Saneamento Básico
- **IBGE** - Instituto Brasileiro de Geografia e Estatística
- **INCRA** - Instituto Nacional de Colonização e Reforma Agrária
- **INPE** - Instituto Nacional de Pesquisas Espaciais
- **DNIT** - Departamento Nacional de Infraestrutura de Transportes
- **ICMBio** - Instituto Chico Mendes de Conservação da Biodiversidade
- **ANM** - Agência Nacional de Mineração
- **ANP** - Agência Nacional do Petróleo, Gás Natural e Biocombustíveis
- E muitos outros...

---

## 🎨 Personalização

### Alterar cores da interface

Edite o arquivo `interface/styles.css` e modifique as variáveis CSS:

```css
:root {
    --primary-color: #2563eb;     /* Cor principal */
    --secondary-color: #1e40af;   /* Cor secundária */
    --success-color: #10b981;     /* Cor de sucesso */
    --warning-color: #f59e0b;     /* Cor de aviso */
    --danger-color: #ef4444;      /* Cor de erro */
}
```

### Adicionar nova ferramenta

1. Adicione a ferramenta no servidor MCP (`mcp_inde_server_main.py`)
2. Crie uma nova seção no HTML (`interface/index.html`)
3. Adicione a lógica JavaScript (`interface/app.js`)
4. Adicione link no menu de navegação

---

## 📝 Notas de Versão

### v1.0.0 (Atual)

**Funcionalidades:**
- ✅ Interface web completa
- ✅ 6 ferramentas MCP integradas
- ✅ Modo demonstração com dados simulados
- ✅ Design responsivo
- ✅ Servidor HTTP embutido
- ✅ Suporte a múltiplos formatos de exportação

**Próximas funcionalidades:**
- 🔄 Conexão real com servidor MCP via WebSocket
- 🔄 Visualização de mapas integrada (Leaflet/OpenLayers)
- 🔄 Cache de resultados
- 🔄 Histórico de consultas
- 🔄 Export de dados para múltiplos formatos

---

## 📞 Suporte

Para problemas, dúvidas ou sugestões:

1. Verifique a seção [Solução de Problemas](#-solução-de-problemas)
2. Consulte a documentação completa em `complete_guide_mcp.md`
3. Revise o manual do usuário em `manual_usuario.md`

---

## 📄 Licença

Este projeto é fornecido como está, para uso educacional e de pesquisa.

---

## 🙏 Agradecimentos

- **INDE** - Infraestrutura Nacional de Dados Espaciais
- **Órgãos Brasileiros** - Por disponibilizarem dados geoespaciais abertos
- **FastMCP** - Framework MCP para Python
- **CrewAI** - Framework para agentes AI

---

**Desenvolvido com ❤️ para facilitar o acesso a dados geoespaciais brasileiros**
