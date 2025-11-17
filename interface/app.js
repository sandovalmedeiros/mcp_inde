// INDE MCP Interface - Main Application
class MCPInterface {
    constructor() {
        this.mcpEndpoint = 'http://localhost:3000/mcp'; // Endpoint do servidor MCP
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupForms();
        this.checkConnection();
    }

    // Navigation
    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const sectionId = link.dataset.section;
                this.showSection(sectionId);

                // Update active state
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }

    showSection(sectionId) {
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => {
            section.classList.remove('active');
        });

        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
        }
    }

    // Forms Setup
    setupForms() {
        // List Services Form
        const listServicesForm = document.getElementById('listServicesForm');
        listServicesForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.listServices();
        });

        // Discover Layers Form
        const discoverLayersForm = document.getElementById('discoverLayersForm');
        discoverLayersForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.discoverLayers();
        });

        // Extract Data Form
        const extractDataForm = document.getElementById('extractDataForm');
        extractDataForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.extractData();
        });

        // Analyze Capabilities Form
        const analyzeCapabilitiesForm = document.getElementById('analyzeCapabilitiesForm');
        analyzeCapabilitiesForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.analyzeCapabilities();
        });

        // Intelligent Analysis Form
        const intelligentAnalysisForm = document.getElementById('intelligentAnalysisForm');
        intelligentAnalysisForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.intelligentAnalysis();
        });

        // Generate Report Form
        const generateReportForm = document.getElementById('generateReportForm');
        generateReportForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateReport();
        });
    }

    // Connection Check
    async checkConnection() {
        const statusElement = document.getElementById('connectionStatus');

        // Simular verificação de conexão (em ambiente real, faria ping ao servidor)
        statusElement.innerHTML = '<i class="fas fa-circle"></i> <span>Modo Demonstração</span>';
        statusElement.classList.remove('connected', 'disconnected');
        statusElement.classList.add('connected');
    }

    // MCP Tool Functions
    async listServices() {
        const orgao = document.getElementById('orgaoFilter').value;
        const resultDiv = document.getElementById('listServicesResult');

        this.showLoading(true);

        try {
            // Simular chamada ao MCP (em ambiente real, usaria fetch/axios)
            const mockData = await this.simulateListServices(orgao);
            this.displayListServicesResult(mockData, resultDiv);
        } catch (error) {
            this.displayError(resultDiv, error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async discoverLayers() {
        const orgao = document.getElementById('layerOrgao').value;
        const serviceName = document.getElementById('layerServiceName').value;
        const resultDiv = document.getElementById('discoverLayersResult');

        this.showLoading(true);

        try {
            const mockData = await this.simulateDiscoverLayers(orgao, serviceName);
            this.displayDiscoverLayersResult(mockData, resultDiv);
        } catch (error) {
            this.displayError(resultDiv, error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async extractData() {
        const orgao = document.getElementById('extractOrgao').value;
        const serviceName = document.getElementById('extractServiceName').value;
        const layer = document.getElementById('extractLayer').value;
        const maxFeatures = document.getElementById('extractMaxFeatures').value;
        const resultDiv = document.getElementById('extractDataResult');

        this.showLoading(true);

        try {
            const mockData = await this.simulateExtractData(orgao, serviceName, layer, maxFeatures);
            this.displayExtractDataResult(mockData, resultDiv);
        } catch (error) {
            this.displayError(resultDiv, error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async analyzeCapabilities() {
        const orgao = document.getElementById('analyzeOrgao').value;
        const resultDiv = document.getElementById('analyzeCapabilitiesResult');

        this.showLoading(true);

        try {
            const mockData = await this.simulateAnalyzeCapabilities(orgao);
            this.displayAnalyzeCapabilitiesResult(mockData, resultDiv);
        } catch (error) {
            this.displayError(resultDiv, error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async intelligentAnalysis() {
        const orgao = document.getElementById('intelligentOrgao').value;
        const objetivo = document.getElementById('intelligentObjetivo').value;
        const resultDiv = document.getElementById('intelligentAnalysisResult');

        this.showLoading(true);

        try {
            const mockData = await this.simulateIntelligentAnalysis(orgao, objetivo);
            this.displayIntelligentAnalysisResult(mockData, resultDiv);
        } catch (error) {
            this.displayError(resultDiv, error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async generateReport() {
        const orgao = document.getElementById('reportOrgao').value;
        const format = document.getElementById('reportFormat').value;
        const resultDiv = document.getElementById('generateReportResult');

        this.showLoading(true);

        try {
            const mockData = await this.simulateGenerateReport(orgao, format);
            this.displayGenerateReportResult(mockData, resultDiv, format);
        } catch (error) {
            this.displayError(resultDiv, error.message);
        } finally {
            this.showLoading(false);
        }
    }

    // Display Functions
    displayListServicesResult(data, container) {
        container.innerHTML = `
            <div class="result-header">
                <h3><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Serviços Encontrados</h3>
            </div>
            <div class="result-content">
                <div class="stat-grid">
                    <div class="stat-item">
                        <span class="stat-value">${data.total_services}</span>
                        <span class="stat-label">Total de Serviços</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${data.orgaos_disponiveis.length}</span>
                        <span class="stat-label">Órgãos Disponíveis</span>
                    </div>
                </div>

                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-building"></i> Órgãos:
                </h4>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem;">
                    ${data.orgaos_disponiveis.map(org =>
                        `<span style="background: var(--primary-color); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">${org}</span>`
                    ).join('')}
                </div>

                <h4 style="margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-list"></i> Serviços (mostrando primeiros 20):
                </h4>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Órgão</th>
                            <th>Tipo</th>
                            <th>Descrição</th>
                            <th>URL</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.services.map(service => `
                            <tr>
                                <td><strong>${service.orgao}</strong></td>
                                <td><span style="background: var(--info-color); color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem;">${service.tipo}</span></td>
                                <td>${service.descricao}</td>
                                <td style="font-size: 0.8rem; max-width: 300px; overflow: hidden; text-overflow: ellipsis;">${service.url}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        container.classList.add('show');
    }

    displayDiscoverLayersResult(data, container) {
        container.innerHTML = `
            <div class="result-header">
                <h3><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Camadas Descobertas</h3>
            </div>
            <div class="result-content">
                <div class="stat-grid">
                    <div class="stat-item">
                        <span class="stat-value">${data.total_layers}</span>
                        <span class="stat-label">Total de Camadas</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${data.service.tipo}</span>
                        <span class="stat-label">Tipo de Serviço</span>
                    </div>
                </div>

                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-server"></i> Informações do Serviço:
                </h4>
                <div style="background: var(--light-bg); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                    <p><strong>Órgão:</strong> ${data.service.orgao}</p>
                    <p><strong>Descrição:</strong> ${data.service.descricao}</p>
                    <p><strong>URL:</strong> <code style="font-size: 0.85rem;">${data.service.url}</code></p>
                </div>

                <h4 style="margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-layer-group"></i> Camadas Disponíveis:
                </h4>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    ${data.layers.map((layer, index) =>
                        `<div style="background: var(--light-bg); padding: 0.75rem 1rem; border-radius: 8px; display: flex; align-items: center; gap: 0.75rem;">
                            <span style="background: var(--primary-color); color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: bold;">${index + 1}</span>
                            <code style="flex: 1;">${layer}</code>
                        </div>`
                    ).join('')}
                </div>
            </div>
        `;
        container.classList.add('show');
    }

    displayExtractDataResult(data, container) {
        const dataset = data.dataset;
        container.innerHTML = `
            <div class="result-header">
                <h3><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Dados Extraídos com Sucesso</h3>
            </div>
            <div class="result-content">
                <div class="stat-grid">
                    <div class="stat-item">
                        <span class="stat-value">${dataset.total_registros}</span>
                        <span class="stat-label">Registros Extraídos</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${dataset.colunas.length}</span>
                        <span class="stat-label">Colunas</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${dataset.geometria_tipo}</span>
                        <span class="stat-label">Tipo de Geometria</span>
                    </div>
                </div>

                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-columns"></i> Colunas do Dataset:
                </h4>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem;">
                    ${dataset.colunas.map(col =>
                        `<span style="background: var(--success-color); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem;">${col}</span>`
                    ).join('')}
                </div>

                <h4 style="margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-eye"></i> Amostra de Dados (primeiro registro):
                </h4>
                <pre style="background: var(--light-bg); padding: 1rem; border-radius: 8px; overflow-x: auto;">${JSON.stringify(dataset.amostra_dados, null, 2)}</pre>

                <div style="margin-top: 1.5rem; padding: 1rem; background: #dbeafe; border-radius: 8px; border-left: 4px solid var(--info-color);">
                    <strong style="color: var(--info-color);"><i class="fas fa-download"></i> Download:</strong>
                    <p style="margin-top: 0.5rem; color: #1e40af;">Use as ferramentas MCP para baixar os dados completos em GeoJSON ou CSV.</p>
                </div>
            </div>
        `;
        container.classList.add('show');
    }

    displayAnalyzeCapabilitiesResult(data, container) {
        const serviceTypesHTML = Object.entries(data.service_types)
            .map(([type, count]) =>
                `<div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--light-bg); border-radius: 8px;">
                    <span><strong>${type}</strong></span>
                    <span style="background: var(--primary-color); color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-weight: bold;">${count}</span>
                </div>`
            ).join('');

        container.innerHTML = `
            <div class="result-header">
                <h3><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Análise de Capacidades</h3>
            </div>
            <div class="result-content">
                <div class="stat-grid">
                    <div class="stat-item">
                        <span class="stat-value">${data.total_services}</span>
                        <span class="stat-label">Total de Serviços</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${Object.keys(data.service_types).length}</span>
                        <span class="stat-label">Tipos de Serviços</span>
                    </div>
                </div>

                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-chart-pie"></i> Distribuição por Tipo:
                </h4>
                <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem;">
                    ${serviceTypesHTML}
                </div>

                <h4 style="margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-layer-group"></i> Serviços com Camadas Analisadas:
                </h4>
                ${data.services_with_layers.map(item => `
                    <div style="background: var(--light-bg); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                        <h5 style="color: var(--primary-color); margin-bottom: 0.5rem;">${item.service.descricao}</h5>
                        <p><strong>Tipo:</strong> ${item.service.tipo} | <strong>Total de Camadas:</strong> ${item.total_layers}</p>
                        <p style="margin-top: 0.5rem;"><strong>Camadas de exemplo:</strong></p>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">
                            ${item.sample_layers.map(layer =>
                                `<code style="background: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.85rem;">${layer}</code>`
                            ).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        container.classList.add('show');
    }

    displayIntelligentAnalysisResult(data, container) {
        container.innerHTML = `
            <div class="result-header">
                <h3><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Análise Inteligente Concluída</h3>
            </div>
            <div class="result-content">
                <div class="alert alert-info">
                    <i class="fas fa-brain"></i>
                    <div>
                        <strong>Órgão Analisado:</strong> ${data.orgao}<br>
                        <strong>Objetivo:</strong> ${data.objetivo}
                    </div>
                </div>

                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-lightbulb"></i> Insights Principais:
                </h4>
                <ul style="list-style: none; padding: 0;">
                    ${data.insights.map(insight =>
                        `<li style="padding: 0.75rem; background: var(--light-bg); border-radius: 8px; margin-bottom: 0.5rem;">
                            <i class="fas fa-check" style="color: var(--success-color);"></i> ${insight}
                        </li>`
                    ).join('')}
                </ul>

                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-tasks"></i> Recomendações:
                </h4>
                <ul style="list-style: none; padding: 0;">
                    ${data.recomendacoes.map(rec =>
                        `<li style="padding: 0.75rem; background: #dbeafe; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid var(--info-color);">
                            <i class="fas fa-arrow-right" style="color: var(--info-color);"></i> ${rec}
                        </li>`
                    ).join('')}
                </ul>

                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-primary);">
                    <i class="fas fa-file-alt"></i> Relatório Completo:
                </h4>
                <div style="background: var(--light-bg); padding: 1rem; border-radius: 8px; max-height: 400px; overflow-y: auto;">
                    <pre style="white-space: pre-wrap; margin: 0;">${data.relatorio_completo}</pre>
                </div>
            </div>
        `;
        container.classList.add('show');
    }

    displayGenerateReportResult(data, container, format) {
        let contentHTML = '';

        if (format === 'markdown') {
            contentHTML = `<pre style="white-space: pre-wrap; line-height: 1.6;">${data}</pre>`;
        } else if (format === 'json') {
            contentHTML = `<pre>${JSON.stringify(JSON.parse(data), null, 2)}</pre>`;
        } else {
            contentHTML = data;
        }

        container.innerHTML = `
            <div class="result-header">
                <h3><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Relatório Gerado</h3>
                <button onclick="app.downloadReport('${format}')" class="btn btn-primary">
                    <i class="fas fa-download"></i> Baixar Relatório
                </button>
            </div>
            <div class="result-content">
                <div style="background: var(--light-bg); padding: 1.5rem; border-radius: 8px;">
                    ${contentHTML}
                </div>
            </div>
        `;
        container.classList.add('show');
    }

    displayError(container, message) {
        container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i>
                <div>
                    <strong>Erro ao processar requisição:</strong><br>
                    ${message}
                </div>
            </div>
        `;
        container.classList.add('show');
    }

    // Helper Functions
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    }

    downloadReport(format) {
        alert(`Funcionalidade de download em desenvolvimento.\nFormato: ${format}`);
    }

    // Mock Data Simulators (substituir por chamadas reais ao MCP)
    async simulateListServices(orgao) {
        await this.delay(1000);
        return {
            total_services: 45,
            orgaos_disponiveis: ["ANATEL", "ANA", "IBGE", "INCRA", "INPE", "DNIT", "ICMBio", "ANM", "ANP"],
            services: [
                { orgao: "ANATEL", tipo: "OWS", descricao: "ANATEL - Agência Nacional de Telecomunicações", url: "https://sistemas.anatel.gov.br/geoserver/ows" },
                { orgao: "ANA", tipo: "WMS", descricao: "ANA - Agência Nacional de Águas", url: "https://www.snirh.gov.br/arcgis/services/INDE/Camadas/MapServer/WMSServer" },
                { orgao: "IBGE", tipo: "WFS", descricao: "IBGE - Instituto Brasileiro de Geografia e Estatística", url: "https://geoservicos.ibge.gov.br/geoserver/wfs" },
                { orgao: "INCRA", tipo: "OWS", descricao: "INCRA - Instituto Nacional de Colonização e Reforma Agrária", url: "https://geoservicos.incra.gov.br/geoserver/ows" },
                { orgao: "INPE", tipo: "WMS", descricao: "INPE - Instituto Nacional de Pesquisas Espaciais", url: "http://www.dpi.inpe.br/terrabrasilis/geoserver/wms" }
            ]
        };
    }

    async simulateDiscoverLayers(orgao, serviceName) {
        await this.delay(1500);
        return {
            service: {
                orgao: orgao,
                tipo: "OWS",
                descricao: `${orgao} - ${serviceName}`,
                url: `https://sistemas.${orgao.toLowerCase()}.gov.br/geoserver/ows`
            },
            total_layers: 12,
            layers: [
                `${orgao.toLowerCase()}:estacoes`,
                `${orgao.toLowerCase()}:municipios`,
                `${orgao.toLowerCase()}:estados`,
                `${orgao.toLowerCase()}:infraestrutura`,
                `${orgao.toLowerCase()}:cobertura`,
                `${orgao.toLowerCase()}:analise_2024`
            ]
        };
    }

    async simulateExtractData(orgao, serviceName, layer, maxFeatures) {
        await this.delay(2000);
        return {
            success: true,
            dataset: {
                servico: { orgao, tipo: "WFS", descricao: serviceName, url: "https://example.com" },
                camada: layer,
                total_registros: parseInt(maxFeatures),
                colunas: ["id", "nome", "tipo", "status", "municipio", "uf", "latitude", "longitude"],
                amostra_dados: {
                    id: "001",
                    nome: "Estação Central",
                    tipo: "Principal",
                    status: "Ativo",
                    municipio: "São Paulo",
                    uf: "SP",
                    latitude: -23.5505,
                    longitude: -46.6333
                },
                geometria_tipo: "Point"
            }
        };
    }

    async simulateAnalyzeCapabilities(orgao) {
        await this.delay(1500);
        return {
            orgao: orgao,
            total_services: 8,
            service_types: {
                "WFS": 3,
                "WMS": 2,
                "OWS": 3
            },
            services_with_layers: [
                {
                    service: {
                        orgao: orgao,
                        tipo: "OWS",
                        descricao: `${orgao} - Serviço Principal`,
                        url: `https://geoservicos.${orgao.toLowerCase()}.gov.br/geoserver/ows`
                    },
                    total_layers: 24,
                    sample_layers: [`${orgao}:layer1`, `${orgao}:layer2`, `${orgao}:layer3`]
                }
            ]
        };
    }

    async simulateIntelligentAnalysis(orgao, objetivo) {
        await this.delay(3000);
        return {
            orgao: orgao,
            objetivo: objetivo,
            datasets_analisados: [`${orgao}:dados_principais`, `${orgao}:historico`],
            insights: [
                `Identificados ${Math.floor(Math.random() * 100 + 50)} datasets relevantes para ${objetivo}`,
                `Cobertura geográfica abrange ${Math.floor(Math.random() * 27)} estados brasileiros`,
                `Dados atualizados com frequência mensal em 78% dos datasets`,
                `Qualidade dos dados classificada como "Alta" em 85% das camadas analisadas`
            ],
            recomendacoes: [
                `Utilizar camadas WFS para extração detalhada de dados`,
                `Aplicar filtros espaciais para otimizar consultas em áreas específicas`,
                `Considerar integração com outras fontes de dados governamentais`,
                `Implementar cache local para datasets frequentemente acessados`
            ],
            relatorio_completo: `Relatório de Análise Inteligente - ${orgao}\n\nObjetivo: ${objetivo}\n\nResumo Executivo:\nA análise automatizada identificou padrões relevantes nos dados do ${orgao}. Os datasets apresentam boa qualidade e cobertura nacional, sendo adequados para análises em larga escala.\n\nPrincipais Descobertas:\n- Alta disponibilidade de serviços (uptime > 95%)\n- Metadados bem documentados\n- Suporte a múltiplos formatos de saída\n\nPróximos Passos:\n1. Validação manual de dados críticos\n2. Integração com pipeline de análise\n3. Configuração de alertas automáticos`
        };
    }

    async simulateGenerateReport(orgao, format) {
        await this.delay(2000);

        if (format === 'markdown') {
            return `# Relatório de Dados Geoespaciais - ${orgao}

## Resumo Executivo
- **Total de Serviços**: 8
- **Tipos de Serviços**: WFS, WMS, OWS
- **Data da Análise**: ${new Date().toLocaleDateString('pt-BR')}

## Distribuição por Tipo de Serviço
- **WFS**: 3 serviços
- **WMS**: 2 serviços
- **OWS**: 3 serviços

## Serviços com Camadas Identificadas

### ${orgao} - Serviço Principal
- **Tipo**: OWS
- **URL**: https://geoservicos.${orgao.toLowerCase()}.gov.br/geoserver/ows
- **Total de Camadas**: 24
- **Camadas de Exemplo**: layer1, layer2, layer3

## Recomendações
1. Para análise detalhada, use serviços WFS que permitem extração de dados
2. Para visualização rápida, utilize serviços WMS
3. Verifique regularmente a disponibilidade dos serviços
4. Considere limitações de performance para datasets grandes

---
*Relatório gerado automaticamente pelo Sistema INDE MCP*`;
        } else if (format === 'json') {
            return JSON.stringify({
                orgao: orgao,
                total_servicos: 8,
                tipos: ["WFS", "WMS", "OWS"],
                data_analise: new Date().toISOString(),
                servicos: [
                    { tipo: "OWS", camadas: 24 }
                ]
            });
        } else {
            return `<h1>Relatório HTML - ${orgao}</h1><p>Relatório em HTML gerado com sucesso!</p>`;
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize Application
const app = new MCPInterface();
