#!/bin/bash

# ============================================================
# Script de Criação do Banco de Dados INDE MCP
# ============================================================
# Descrição: Executa todos os scripts SQL na ordem correta
# Autor: Sistema INDE MCP
# Data: 2025-11-17
# ============================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para exibir mensagens
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Banner
echo "============================================================"
echo "  INDE MCP - Database Creation Script"
echo "  Infraestrutura Nacional de Dados Espaciais"
echo "============================================================"
echo ""

# Verificar se as variáveis de ambiente estão definidas
if [ -z "$DB_HOST" ]; then
    DB_HOST="localhost"
    print_warning "DB_HOST not set, using default: localhost"
fi

if [ -z "$DB_PORT" ]; then
    DB_PORT="5432"
    print_warning "DB_PORT not set, using default: 5432"
fi

if [ -z "$DB_NAME" ]; then
    print_error "DB_NAME environment variable is not set!"
    echo "Usage: DB_NAME=mydb DB_USER=myuser DB_PASSWORD=mypass ./create_database.sh"
    exit 1
fi

if [ -z "$DB_USER" ]; then
    print_error "DB_USER environment variable is not set!"
    exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
    print_warning "DB_PASSWORD not set, you may be prompted for password"
    export PGPASSWORD=""
else
    export PGPASSWORD="$DB_PASSWORD"
fi

# Diretório dos schemas
SCHEMA_DIR="$(dirname "$0")/schemas"

if [ ! -d "$SCHEMA_DIR" ]; then
    print_error "Schema directory not found: $SCHEMA_DIR"
    exit 1
fi

# Função para executar SQL
execute_sql() {
    local file=$1
    local description=$2

    print_info "Executing: $description"
    print_info "File: $(basename $file)"

    if [ ! -f "$file" ]; then
        print_error "File not found: $file"
        return 1
    fi

    if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$file" > /dev/null 2>&1; then
        print_success "$description completed!"
        return 0
    else
        print_error "$description failed!"
        print_error "Check the file: $file"
        return 1
    fi
}

# Testar conexão com o banco
print_info "Testing database connection..."
if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" > /dev/null 2>&1; then
    print_error "Cannot connect to database!"
    print_error "Host: $DB_HOST:$DB_PORT"
    print_error "Database: $DB_NAME"
    print_error "User: $DB_USER"
    exit 1
fi
print_success "Database connection successful!"
echo ""

# Perguntar ao usuário se deseja continuar
read -p "Do you want to create/recreate the database schema? [y/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Operation cancelled by user"
    exit 0
fi

# Perguntar se deseja dropar as tabelas existentes
read -p "Drop existing tables if they exist? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Dropping existing tables..."
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" << EOF
-- Drop tables in reverse order (respecting foreign keys)
DROP TABLE IF EXISTS t_publicacao_municipios CASCADE;
DROP TABLE IF EXISTS t_municipios CASCADE;
DROP TABLE IF EXISTS t_anos CASCADE;
DROP TABLE IF EXISTS t_tipo_mapa CASCADE;
DROP TABLE IF EXISTS t_classe_mapa CASCADE;

-- Drop functions
DROP FUNCTION IF EXISTS atualizar_data_modificacao() CASCADE;
DROP FUNCTION IF EXISTS calcular_densidade_demografica() CASCADE;
DROP FUNCTION IF EXISTS atualizar_data_ultima_atualizacao() CASCADE;
DROP FUNCTION IF EXISTS obter_estatisticas_municipio(VARCHAR) CASCADE;
EOF
    print_success "Existing tables dropped!"
    echo ""
fi

# Contador de sucesso/erro
SUCCESS_COUNT=0
ERROR_COUNT=0

# Executar scripts na ordem
print_info "Starting database schema creation..."
echo ""

# 1. Tabelas de referência
if execute_sql "$SCHEMA_DIR/01_create_reference_tables.sql" "Creating reference tables"; then
    ((SUCCESS_COUNT++))
else
    ((ERROR_COUNT++))
fi
echo ""

# 2. Tabela de municípios
if execute_sql "$SCHEMA_DIR/02_create_municipios.sql" "Creating municipalities table"; then
    ((SUCCESS_COUNT++))
else
    ((ERROR_COUNT++))
fi
echo ""

# 3. Tabela de publicações municipais
if execute_sql "$SCHEMA_DIR/03_create_publicacao_municipios.sql" "Creating municipal publications table"; then
    ((SUCCESS_COUNT++))
else
    ((ERROR_COUNT++))
fi
echo ""

# Resumo
echo "============================================================"
echo "  Execution Summary"
echo "============================================================"
print_success "Successful: $SUCCESS_COUNT"
if [ $ERROR_COUNT -gt 0 ]; then
    print_error "Failed: $ERROR_COUNT"
else
    print_info "Failed: $ERROR_COUNT"
fi
echo "============================================================"
echo ""

if [ $ERROR_COUNT -eq 0 ]; then
    print_success "Database schema created successfully!"
    echo ""
    print_info "Next steps:"
    echo "  1. Populate t_municipios with IBGE data"
    echo "  2. Import initial publications data"
    echo "  3. Verify data integrity"
    echo ""
    print_info "Useful queries:"
    echo "  - List all tables: \\dt"
    echo "  - List all views: \\dv"
    echo "  - List all functions: \\df"
    echo "  - Describe table: \\d t_municipios"
    exit 0
else
    print_error "Some errors occurred during schema creation"
    print_warning "Please check the error messages above"
    exit 1
fi
