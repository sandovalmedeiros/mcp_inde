# 🚀 Guia Rápido - INDE MCP Interface

Comece a usar a interface INDE MCP em 3 minutos!

---

## ⚡ Início Rápido (3 passos)

### 1️⃣ Iniciar o Servidor da Interface

```bash
cd /home/user/mcp_inde/interface
python3 server.py
```

Você verá:
```
======================================================================
🌐 INDE MCP - Servidor de Interface Web
======================================================================

✅ Servidor rodando em: http://localhost:8000
📁 Diretório: /home/user/mcp_inde/interface

📖 Para acessar a interface:
   Abra seu navegador e acesse: http://localhost:8000
```

### 2️⃣ Abrir no Navegador

Abra seu navegador favorito e acesse:
```
http://localhost:8000
```

### 3️⃣ Começar a Explorar!

No dashboard, clique em **"Listar Serviços"** e explore os dados geoespaciais brasileiros!

---

## 🎯 Casos de Uso Comuns

### Caso 1: Listar todos os serviços da ANATEL

1. Clique em **"Listar Serviços"** no menu lateral
2. Digite `ANATEL` no campo "Filtrar por Órgão"
3. Clique em **"Listar Serviços"**
4. Veja todos os serviços geoespaciais da ANATEL!

### Caso 2: Descobrir camadas de um serviço

1. Clique em **"Descobrir Camadas"**
2. Preencha:
   - **Órgão:** `ANATEL`
   - **Nome do Serviço:** `telecomunicações`
3. Clique em **"Descobrir Camadas"**
4. Veja todas as camadas disponíveis!

### Caso 3: Extrair dados de uma camada

1. Clique em **"Extrair Dados"**
2. Preencha:
   - **Órgão:** `ANATEL`
   - **Nome do Serviço:** `telecomunicações`
   - **Camada:** `anatel:estacoes`
   - **Máximo de Registros:** `1000`
3. Clique em **"Extrair Dados"**
4. Veja os dados extraídos com estatísticas!

### Caso 4: Gerar relatório automático

1. Clique em **"Gerar Relatório"**
2. Digite o órgão: `ANATEL`
3. Escolha o formato: `Markdown`
4. Clique em **"Gerar Relatório"**
5. Veja o relatório completo formatado!

---

## 🔧 Configurar com Claude Desktop (Opcional)

Para usar o servidor MCP diretamente no Claude Desktop:

### macOS
```bash
# 1. Editar configuração
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Adicionar configuração do INDE MCP
# (Copie o conteúdo de mcp_config.json)

# 3. Reiniciar Claude Desktop
```

### Linux
```bash
# 1. Editar configuração
nano ~/.config/Claude/claude_desktop_config.json

# 2. Adicionar configuração do INDE MCP
# (Copie o conteúdo de mcp_config.json)

# 3. Reiniciar Claude Desktop
```

### Windows
```powershell
# 1. Editar configuração
notepad %APPDATA%\Claude\claude_desktop_config.json

# 2. Adicionar configuração do INDE MCP
# (Copie o conteúdo de mcp_config.json)

# 3. Reiniciar Claude Desktop
```

**Conteúdo a adicionar:**

```json
{
  "mcpServers": {
    "inde-geospatial": {
      "command": "python3",
      "args": [
        "/home/user/mcp_inde/mcp_inde_server_main.py"
      ],
      "env": {
        "PYTHONPATH": "/home/user/mcp_inde",
        "CATALOG_PATH": "/home/user/mcp_inde/catalogo_inde.yaml"
      }
    }
  }
}
```

**⚠️ Substitua `/home/user/mcp_inde/` pelo caminho real no seu sistema!**

---

## 📚 Documentação Completa

- **Interface Web:** [INTERFACE_README.md](INTERFACE_README.md)
- **Manual Completo MCP:** [complete_guide_mcp.md](complete_guide_mcp.md)
- **Manual do Usuário:** [manual_usuario.md](manual_usuario.md)

---

## 💡 Dicas

### ✅ DO (Faça)
- Comece com poucos registros (100-500) para testes
- Use filtros para encontrar serviços rapidamente
- Explore o Dashboard para entender as funcionalidades
- Leia as tooltips e mensagens de ajuda

### ❌ DON'T (Não faça)
- Não extraia milhares de registros de uma vez
- Não use espaços ou caracteres especiais nos nomes
- Não execute múltiplas análises inteligentes simultaneamente
- Não feche o servidor enquanto a interface está em uso

---

## 🆘 Problemas Comuns

### Porta ocupada?
```bash
# Use outra porta
python3 server.py 8080
```

### Interface não abre?
```bash
# Verifique se o servidor está rodando
# Deve mostrar: "Servidor rodando em: http://localhost:8000"

# Tente acessar diretamente
curl http://localhost:8000
```

### Dados não aparecem?
- Verifique a ortografia do nome do órgão
- Tente outro serviço/camada
- Reduza o número máximo de registros

---

## 🎉 Pronto!

Você está pronto para explorar dados geoespaciais brasileiros!

**Próximos passos:**
1. Explore diferentes órgãos (ANA, IBGE, INCRA, etc.)
2. Descubra quais camadas estão disponíveis
3. Extraia dados para suas análises
4. Gere relatórios automáticos

**Boa exploração! 🇧🇷** 🗺️
