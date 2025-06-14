#!/bin/bash

# INDE MCP Server - Setup Script
# Configuração automática do ambiente

set -e

echo "🚀 INDE MCP Server - Setup Automático"
echo "======================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar Python
check_python() {
    log_info "Verificando instalação do Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python $PYTHON_VERSION encontrado"
        
        # Verificar versão mínima (3.8+)
        MIN_VERSION="3.8"
        if python3 -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"; then
            log_success "Versão do Python compatível (>= 3.8)"
        else
            log_error "Python 3.8+ requerido. Versão atual: $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "Python3 não encontrado. Instale Python 3.8+ primeiro."
        exit 1
    fi
}

# Criar ambiente virtual
setup_virtualenv() {
    log_info "Configurando ambiente virtual..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_success "Ambiente virtual criado"
    else
        log_warning "Ambiente virtual já existe"
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    log_success "Ambiente virtual ativado"
    
    # Atualizar pip
    python -m pip install --upgrade pip
    log_success "Pip atualizado"
}

# Instalar dependências
install_dependencies() {
    log_info "Instalando dependências..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Dependências instaladas"
    else
        log_warning "requirements.txt não encontrado. Instalando dependências básicas..."
        
        # Dependências essenciais
        pip install fastmcp>=0.9.0
        pip install crewai>=0.28.0
        pip install pandas>=1.5.0
        pip install requests>=2.28.0
        pip install PyYAML>=6.0
        pip install aiohttp>=3.8.0
        pip install python-dotenv>=1.0.0
        
        log_success "Dependências básicas instaladas"
    fi
}

# Configurar arquivo .env
setup_env() {
    log_info "Configurando arquivo de ambiente..."
    
    if [ ! -f ".env" ]; then
        cat > .env << 'EOF'
# INDE MCP Server Configuration

# OpenAI API (obrigatório para agentes)
OPENAI_API_KEY=your_openai_api_key_here

# Servidor MCP
MCP_HOST=localhost
MCP_PORT=8000

# Configurações de performance
MAX_FEATURES=1000
REQUEST_TIMEOUT=30
MAX_CONCURRENT=5

# Cache (opcional)
USE_REDIS=false
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO

# Catálogo INDE
INDE_CATALOG_PATH=./catalogo_inde.yaml
CACHE_TTL=3600

# CrewAI
OPENAI_MODEL=gpt-4
CREW_VERBOSE=true
EOF
        log_success "Arquivo .env criado"
        log_warning "Configure sua OPENAI_API_KEY no arquivo .env"
    else
        log_warning "Arquivo .env já existe"
    fi
}

# Criar catálogo de exemplo
setup_catalog() {
    log_info "Configurando catálogo INDE..."
    
    if [ ! -f "catalogo_inde.yaml" ]; then
        cat > catalogo_inde.yaml << 'EOF'
# Catálogo de Serviços INDE - Exemplo
# Para uso completo, substitua pelos dados reais da INDE

- descricao: "ANATEL - Agência Nacional de Telecomunicações"
  url: "https://sistemas.anatel.gov.br/geoserver/ows"
  tipo: "OWS"

- descricao: "ANA - Agência Nacional de Águas e Saneamento Básico"
  url: "https://metadados.snirh.gov.br/geoserver/wfs"
  tipo: "WFS"

- descricao: "IBGE - Instituto Brasileiro de Geografia e Estatística"
  url: "https://geoservicos.ibge.gov.br/geoserver/wfs"
  tipo: "WFS"

- descricao: "INCRA - Instituto Nacional de Colonização e Reforma Agrária"
  url: "https://certificacao.incra.gov.br/csv_shp/export_shp.py"
  tipo: "WFS"

- descricao: "ICMBio - Instituto Chico Mendes de Conservação da Biodiversidade"
  url: "https://geoservicos.icmbio.gov.br/geoserver/ows"
  tipo: "OWS"

# Adicione mais serviços conforme necessário
EOF
        log_success "Catálogo de exemplo criado"
        log_info "Edite catalogo_inde.yaml para adicionar mais serviços"
    else
        log_warning "Catálogo já existe"
    fi
}

# Criar estrutura de diretórios
setup_directories() {
    log_info "Criando estrutura de diretórios..."
    
    mkdir -p logs
    mkdir -p reports
    mkdir -p cache
    mkdir -p tests
    mkdir -p docs
    
    log_success "Diretórios criados"
}

# Verificar dependências opcionais
check_optional_deps() {
    log_info "Verificando dependências opcionais..."
    
    # Redis
    if command -v redis-server &> /dev/null; then
        log_success "Redis encontrado (cache distribuído disponível)"
    else
        log_warning "Redis não encontrado (cache em memória será usado)"
    fi
    
    # Docker
    if command -v docker &> /dev/null; then
        log_success "Docker encontrado (deploy containerizado disponível)"
    else
        log_warning "Docker não encontrado (deploy manual disponível)"
    fi
}

# Executar testes básicos
run_basic_tests() {
    log_info "Executando testes básicos..."
    
    # Testar importações Python
    python3 -c "
import sys
try:
    import yaml
    import pandas
    import requests
    print('✅ Dependências básicas OK')
except ImportError as e:
    print(f'❌ Erro de importação: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        log_success "Testes de importação passaram"
    else
        log_error "Falha nos testes de importação"
        exit 1
    fi
}

# Gerar scripts de conveniência
create_convenience_scripts() {
    log_info "Criando scripts de conveniência..."
    
    # Script para iniciar servidor
    cat > start_server.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando INDE MCP Server..."
source venv/bin/activate
python mcp_inde_server.py
EOF
    chmod +x start_server.sh
    
    # Script para demo
    cat > run_demo.sh << 'EOF'
#!/bin/bash
echo "🎮 Executando demonstração..."
source venv/bin/activate
python demo_script.py
EOF
    chmod +x run_demo.sh
    
    # Script para testes
    cat > run_tests.sh << 'EOF'
#!/bin/bash
echo "🧪 Executando testes..."
source venv/bin/activate
python -m pytest tests/ -v
EOF
    chmod +x run_tests.sh
    
    log_success "Scripts de conveniência criados"
}

# Mostrar instruções finais
show_final_instructions() {
    echo ""
    echo "🎉 Setup concluído com sucesso!"
    echo "=============================="
    echo ""
    echo "📋 Próximos passos:"
    echo ""
    echo "1️⃣  Configure sua OPENAI_API_KEY:"
    echo "   📝 Edite o arquivo .env"
    echo "   🔑 Adicione sua chave da OpenAI"
    echo ""
    echo "2️⃣  Execute a demonstração:"
    echo "   🎮 ./run_demo.sh"
    echo ""
    echo "3️⃣  Inicie o servidor MCP:"
    echo "   🚀 ./start_server.sh"
    echo ""
    echo "4️⃣  Execute testes (opcional):"
    echo "   🧪 ./run_tests.sh"
    echo ""
    echo "📚 Documentação:"
    echo "   📖 README.md - Documentação técnica"
    echo "   📋 MANUAL.md - Manual do usuário"
    echo ""
    echo "🔗 Arquivos importantes:"
    echo "   ⚙️  .env - Configurações"
    echo "   📊 catalogo_inde.yaml - Catálogo de serviços"
    echo "   🗂️  logs/ - Logs do sistema"
    echo "   📄 reports/ - Relatórios gerados"
    echo ""
    log_success "Sistema pronto para uso!"
}

# Função principal
main() {
    echo ""
    log_info "Iniciando configuração do INDE MCP Server..."
    echo ""
    
    check_python
    setup_virtualenv
    install_dependencies
    setup_env
    setup_catalog
    setup_directories
    check_optional_deps
    run_basic_tests
    create_convenience_scripts
    
    show_final_instructions
}

# Verificar se script está sendo executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
