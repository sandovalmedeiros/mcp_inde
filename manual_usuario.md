# 📚 Manual do Usuário - Catálogo INDE
## Catálogo de Serviços Geoespaciais por Órgão

---

## 📖 **Índice**

1. [Visão Geral](#visão-geral)
2. [Como Começar](#como-começar)
3. [Funcionalidades Principais](#funcionalidades-principais)
4. [Guia Passo a Passo](#guia-passo-a-passo)
5. [Tipos de Serviços](#tipos-de-serviços)
6. [Formatos de Download](#formatos-de-download)
7. [Solução de Problemas](#solução-de-problemas)
8. [Dicas e Truques](#dicas-e-truques)

---

## 🎯 **Visão Geral**

O **Catálogo INDE** é uma aplicação web interativa que permite:

- 🗺️ **Visualizar mapas** de dados geoespaciais brasileiros
- 📊 **Explorar dados** em tabelas interativas  
- 💾 **Baixar datasets** em múltiplos formatos
- 🔍 **Pesquisar** por órgão ou descrição
- 📋 **Ver informações detalhadas** através de tooltips

### **Órgãos Disponíveis**
ANATEL • ANA • IBGE • INCRA • INPE • DNIT • ICMBio • e muitos outros!

---

## 🚀 **Como Começar**

### **Passo 1: Acesse a Aplicação**
Abra a aplicação no seu navegador web.

### **Passo 2: Interface Principal**
Você verá três seções principais:
- **🔍 Filtros** - Para encontrar o serviço desejado
- **📋 Informações** - Detalhes do serviço selecionado  
- **🎯 Ações** - O que você pode fazer com os dados

---

## ⭐ **Funcionalidades Principais**

### **1. 🗺️ Visualizar Mapa**
- Mapas interativos com dados geográficos
- Tooltips informativos ao passar o mouse
- Controles de camadas
- Zoom e navegação

### **2. 📊 Visualizar Dados**
- Tabelas com todos os registros
- Filtros por texto
- Seleção de colunas
- Estatísticas automáticas

### **3. 💾 Baixar Dados**
- **CSV** - Para Excel/Google Sheets
- **GeoJSON** - Para QGIS/ArcGIS
- **JSON** - Para desenvolvimento
- **URLs diretas** - Para download manual

---

## 📝 **Guia Passo a Passo**

### **🔍 Encontrando Dados**

#### **Passo 1: Pesquisar**
- Digite no campo **"🔍 Pesquisar"**
- Exemplos: "telecomunicações", "recursos hídricos", "ANATEL"

#### **Passo 2: Selecionar Órgão**
- Escolha o órgão no menu **"📌 Selecione o Órgão"**
- Os órgãos são filtrados automaticamente

#### **Passo 3: Escolher Serviço**
- Selecione o serviço específico no menu **"🧭 Escolha o serviço"**

### **📋 Configurando o Serviço**

#### **Para Serviços OWS:**
1. O sistema **detecta automaticamente** os tipos disponíveis
2. Escolha entre **WFS** (dados) ou **WMS** (imagem)
3. Use **"WMS (Forçado)"** se WFS estiver lento

#### **Para Serviços WFS/WMS:**
1. O sistema **lista as camadas** disponíveis automaticamente
2. Selecione a camada desejada
3. Configure as opções conforme necessário

### **⚙️ Opções de Configuração**

- **📋 Tooltips**: Liga/desliga informações ao passar o mouse (apenas WFS)
- **📊 Máx. registros**: Limite de dados para carregamento (100-5000)

---

## 🌐 **Tipos de Serviços**

### **🗺️ WFS (Web Feature Service)**
**O que é:** Dados vetoriais com informações detalhadas

**Vantagens:**
- ✅ Tooltips informativos
- ✅ Download de dados
- ✅ Visualização em tabela
- ✅ Filtros e pesquisa

**Desvantagens:**
- ⚠️ Carregamento mais lento
- ⚠️ Pode falhar com muitos dados

**Melhor para:** Análise detalhada, download de dados

### **🖼️ WMS (Web Map Service)**
**O que é:** Imagens de mapa pré-renderizadas

**Vantagens:**
- ✅ Carregamento rápido
- ✅ Sempre funciona
- ✅ Menos uso de dados

**Desvantagens:**
- ❌ Sem tooltips
- ❌ Sem download direto
- ❌ Apenas visualização

**Melhor para:** Visualização rápida, mapas de contexto

### **🔧 OWS (OGC Web Services)**
**O que é:** Endpoint que oferece múltiplos serviços

**Como funciona:**
1. Sistema detecta WFS e/ou WMS disponíveis
2. Você escolhe qual usar
3. Opção "WMS (Forçado)" para garantir funcionamento

### **🆚 WFS vs WMS - Quando Usar Cada Um?**

| Situação | Use WFS | Use WMS |
|----------|---------|---------|
| Analisar dados detalhados | ✅ | ❌ |
| Download para análise | ✅ | ❌ |
| Visualização rápida | ❌ | ✅ |
| Conexão lenta | ❌ | ✅ |
| Muitos dados (>5000 registros) | ⚠️ | ✅ |
| Informações ao clicar/hover | ✅ | ❌ |

---

## 💾 **Formatos de Download**

### **📊 CSV (Comma Separated Values)**
- **Para que serve:** Análise em planilhas
- **Programas:** Excel, Google Sheets, LibreOffice
- **Contém:** Apenas dados tabulares (sem geometria)

### **🗺️ GeoJSON**
- **Para que serve:** Análise geoespacial
- **Programas:** QGIS, ArcGIS, Google Earth Pro
- **Contém:** Dados + geometria + propriedades

### **📄 JSON**
- **Para que serve:** Desenvolvimento/APIs
- **Programas:** Editores de código, aplicações web
- **Contém:** Dados estruturados

### **🔗 URLs Manuais**
Quando os downloads automáticos não funcionam:
- **GeoJSON**: `...&outputFormat=application/json`
- **CSV**: `...&outputFormat=csv`
- **Shapefile**: `...&outputFormat=SHAPE-ZIP`

---

## 🛠️ **Solução de Problemas**

### **❌ "Erro ao carregar mapa"**

**Causas possíveis:**
- Serviço temporariamente indisponível
- Camada incorreta selecionada
- Problema de rede

**Soluções:**
1. ✅ Tente **"WMS (Forçado)"** para OWS
2. ✅ Selecione outra camada
3. ✅ Aguarde alguns minutos e tente novamente
4. ✅ Verifique sua conexão com internet

### **⏰ "Timeout ao carregar dados"**

**Causas:**
- Muitos dados sendo carregados
- Servidor lento
- Conexão instável

**Soluções:**
1. ✅ Reduza o **"Máx. registros"** para 500 ou menos
2. ✅ Use **WMS** em vez de WFS
3. ✅ Tente em outro horário

### **📭 "Nenhum dado encontrado"**

**Causas:**
- Camada vazia
- Filtros muito restritivos
- Área geográfica sem dados

**Soluções:**
1. ✅ Tente outra camada
2. ✅ Remova filtros aplicados
3. ✅ Verifique se escolheu a camada correta

### **💾 "Download não funciona"**

**Soluções:**
1. ✅ Use as **URLs manuais** fornecidas
2. ✅ Tente formato diferente (CSV em vez de GeoJSON)
3. ✅ Reduza o número de registros

---

## 💡 **Dicas e Truques**

### **🚀 Para Melhor Performance:**

1. **📊 Limite registros**: Para análise inicial, use 500-1000 registros
2. **🖼️ Use WMS**: Para visualização rápida, sempre prefira WMS
3. **🔍 Seja específico**: Use filtros para reduzir a quantidade de dados
4. **⏱️ Horário**: Evite horários de pico (9h-11h, 14h-16h)

### **📊 Para Análise de Dados:**

1. **📋 Comece com amostra**: Carregue poucos dados primeiro para entender a estrutura
2. **📈 Use filtros**: Filtre por município/estado para dados específicos
3. **📑 Selecione colunas**: Escolha apenas as colunas relevantes para sua análise
4. **💾 Download gradual**: Para datasets grandes, baixe por partes

### **🗺️ Para Visualização:**

1. **🎯 Tooltips**: Sempre habilite para WFS - vê informações ao passar o mouse
2. **🔧 WMS (Forçado)**: Use quando WFS estiver lento
3. **📱 Zoom**: Use zoom para áreas específicas antes de carregar dados
4. **🎨 Sobreposição**: Carregue camadas WMS como contexto

### **🔍 Para Pesquisa:**

1. **🏢 Por órgão**: Digite "ANATEL", "ANA", "IBGE" na pesquisa
2. **📍 Por região**: "São Paulo", "Nordeste", "Amazônia"
3. **🎯 Por tema**: "telecomunicações", "recursos hídricos", "agricultura"
4. **🔢 Por código**: Códigos técnicos específicos quando conhecidos

---

## 📞 **Precisa de Ajuda?**

### **🔍 Use o Debug Info**
- Expanda a seção **"🔍 Informações de Debug"**
- Copie as informações para relatar problemas

### **📋 Informações Úteis para Suporte**
- Nome do órgão e serviço
- Tipo de erro (mapa, dados, download)
- Navegador utilizado
- Informações do Debug

---

## 🎉 **Aproveite a Aplicação!**

O Catálogo INDE foi desenvolvido para facilitar o acesso aos dados geoespaciais brasileiros. Com essas funcionalidades, você pode:

- 🔬 **Pesquisar** dados governamentais
- 📊 **Analisar** informações espaciais  
- 💾 **Baixar** datasets para suas pesquisas
- 🗺️ **Visualizar** dados no mapa

**Boa exploração dos dados geoespaciais do Brasil!** 🇧🇷✨