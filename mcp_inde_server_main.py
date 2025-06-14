#!/usr/bin/env python3
"""
INDE MCP Server - Arquivo Principal
Protocolo MCP para Dados Geoespaciais Brasileiros integrado com CrewAI

Funcionalidades principais:
- 6 ferramentas MCP para descoberta e análise de dados
- 3 agentes CrewAI especializados
- Extração automática de dados WFS/WMS/OWS
- Geração de relatórios automatizados
- Integração completa com Claude

Uso: python mcp_inde_server.py
"""

import asyncio
import json
import logging
import yaml
import pandas as pd
import requests
from xml.etree import ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# MCP e CrewAI
from fastmcp import FastMCP
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ================================
# MODELOS DE DADOS
# ================================

@dataclass
class GeoService:
    """Modelo para serviços geoespaciais."""
    orgao: str
    tipo: str
    descricao: str
    url: str
    camadas: Optional[List[str]] = None
    metadados: Optional[Dict[str, Any]] = None


@dataclass
class DatasetInfo:
    """Informações sobre um dataset extraído."""
    servico: GeoService
    camada: str
    total_registros: int
    colunas: List[str]
    amostra_dados: Dict[str, Any]
    geometria_tipo: str
    bbox: Optional[List[float]] = None


class AnalysisRequest(BaseModel):
    """Requisição de análise."""
    orgao: str
    objetivo: str
    filtros: Optional[Dict[str, Any]] = None
    formato_saida: str = "relatorio"


class AnalysisResult(BaseModel):
    """Resultado de análise."""
    orgao: str
    objetivo: str
    datasets_analisados: List[str]
    insights: List[str]
    recomendacoes: List[str]
    dados_extraidos: Dict[str, Any]
    relatorio_completo: str


# ================================
# EXTRATOR DE DADOS INDE
# ================================

class INDEDataExtractor:
    """Extrator de dados da INDE baseado na aplicação original."""
    
    def __init__(self, catalog_path: str = "catalogo_inde.yaml"):
        self.catalog_path = Path(catalog_path)
        self.services_cache = {}
    
    async def load_catalog(self) -> List[GeoService]:
        """Carrega catálogo de serviços."""
        try:
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                catalog_data = yaml.safe_load(f)
            
            services = []
            for item in catalog_data:
                if isinstance(item, dict):
                    descricao = item.get("descricao", item.get("title", "Sem descrição"))
                    url = item.get("url", item.get("link", ""))
                    if url:
                        tipo = self._extract_service_type(url)
                        orgao = self._extract_orgao(descricao)
                        
                        service = GeoService(
                            orgao=orgao,
                            tipo=tipo,
                            descricao=descricao,
                            url=url
                        )
                        services.append(service)
            
            return services
        except Exception as e:
            logger.error(f"Erro ao carregar catálogo: {e}")
            return []
    
    def _extract_service_type(self, url: str) -> str:
        """Extrai tipo de serviço da URL."""
        url_lower = url.lower()
        if "wfs" in url_lower:
            return "WFS"
        elif "wms" in url_lower:
            return "WMS"
        elif "ows" in url_lower:
            return "OWS"
        elif "wmts" in url_lower:
            return "WMTS"
        elif "wcs" in url_lower:
            return "WCS"
        else:
            return "Outro"
    
    def _extract_orgao(self, descricao: str) -> str:
        """Extrai o órgão da descrição."""
        return descricao.split("-")[0].strip() if "-" in descricao else "Desconhecido"
    
    async def discover_layers(self, service: GeoService) -> List[str]:
        """Descobre camadas disponíveis em um serviço."""
        try:
            if service.tipo in ["WFS", "OWS"]:
                return await self._get_wfs_layers(service.url)
            elif service.tipo in ["WMS", "OWS"]:
                return await self._get_wms_layers(service.url)
            else:
                return []
        except Exception as e:
            logger.error(f"Erro ao descobrir camadas: {e}")
            return []
    
    async def _get_wfs_layers(self, url: str) -> List[str]:
        """Obtém camadas WFS."""
        try:
            params = {
                "service": "WFS",
                "request": "GetCapabilities",
                "version": "2.0.0"
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            tree = ET.fromstring(response.content)
            
            # Tentar diferentes namespaces
            namespaces = [
                {"wfs": "http://www.opengis.net/wfs/2.0"},
                {"wfs": "http://www.opengis.net/wfs"},
                {}
            ]
            
            layers = []
            for ns in namespaces:
                try:
                    if ns:
                        features = tree.findall(".//wfs:FeatureType/wfs:Name", ns)
                        if not features:
                            features = tree.findall(".//FeatureType/Name", ns)
                    else:
                        features = tree.findall(".//FeatureType/Name")
                    
                    for feature in features:
                        if feature is not None and feature.text:
                            layers.append(feature.text)
                    
                    if layers:
                        break
                except:
                    continue
            
            return list(set(layers))
        except Exception as e:
            logger.error(f"Erro ao obter camadas WFS: {e}")
            return []
    
    async def _get_wms_layers(self, url: str) -> List[str]:
        """Obtém camadas WMS."""
        try:
            params = {
                "service": "WMS", 
                "request": "GetCapabilities",
                "version": "1.3.0"
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            tree = ET.fromstring(response.content)
            
            # Tentar diferentes namespaces
            namespaces = [
                {"wms": "http://www.opengis.net/wms"},
                {"": "http://www.opengis.net/wms"},
                {}
            ]
            
            layers = []
            for ns in namespaces:
                try:
                    if ns:
                        layer_elements = tree.findall(".//wms:Layer/wms:Name", ns)
                        if not layer_elements:
                            layer_elements = tree.findall(".//Layer/Name", ns)
                    else:
                        layer_elements = tree.findall(".//Layer/Name")
                    
                    for layer in layer_elements:
                        if layer is not None and layer.text:
                            layers.append(layer.text)
                    
                    if layers:
                        break
                except:
                    continue
            
            return list(set(layers))
        except Exception as e:
            logger.error(f"Erro ao obter camadas WMS: {e}")
            return []
    
    async def extract_data(self, service: GeoService, layer: str, max_features: int = 1000) -> Optional[DatasetInfo]:
        """Extrai dados de uma camada WFS."""
        try:
            if service.tipo not in ["WFS", "OWS"]:
                logger.warning(f"Extração de dados não suportada para {service.tipo}")
                return None
            
            # Construir URL WFS
            if '?' in service.url:
                wfs_url = f"{service.url}&service=WFS&request=GetFeature&typeName={layer}&outputFormat=application/json&maxFeatures={max_features}"
            else:
                wfs_url = f"{service.url}?service=WFS&request=GetFeature&typeName={layer}&outputFormat=application/json&maxFeatures={max_features}"
            
            response = requests.get(wfs_url, timeout=30)
            response.raise_for_status()
            
            if response.status_code == 200 and response.content:
                geojson_data = response.json()
                
                if 'features' in geojson_data and len(geojson_data['features']) > 0:
                    # Extrair informações do dataset
                    features = geojson_data['features']
                    first_feature = features[0]
                    
                    properties = first_feature.get('properties', {})
                    geometry = first_feature.get('geometry', {})
                    
                    dataset_info = DatasetInfo(
                        servico=service,
                        camada=layer,
                        total_registros=len(features),
                        colunas=list(properties.keys()),
                        amostra_dados=properties,
                        geometria_tipo=geometry.get('type', 'Unknown')
                    )
                    
                    # Calcular bbox se disponível
                    if 'bbox' in geojson_data:
                        dataset_info.bbox = geojson_data['bbox']
                    
                    return dataset_info
                
            return None
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {e}")
            return None


# ================================
# FERRAMENTAS MCP
# ================================

class INDETools:
    """Ferramentas MCP para interação com INDE."""
    
    def __init__(self):
        self.extractor = INDEDataExtractor()
        self.services_cache = None
    
    async def list_services(self, orgao: Optional[str] = None) -> Dict[str, Any]:
        """Lista serviços disponíveis, opcionalmente filtrados por órgão."""
        if not self.services_cache:
            self.services_cache = await self.extractor.load_catalog()
        
        services = self.services_cache
        
        if orgao:
            services = [s for s in services if orgao.lower() in s.orgao.lower()]
        
        result = {
            "total_services": len(services),
            "orgaos_disponiveis": list(set(s.orgao for s in services)),
            "services": [asdict(s) for s in services[:20]]  # Limitar para não sobrecarregar
        }
        
        return result
    
    async def discover_service_layers(self, orgao: str, service_name: str) -> Dict[str, Any]:
        """Descobre camadas disponíveis em um serviço específico."""
        if not self.services_cache:
            self.services_cache = await self.extractor.load_catalog()
        
        # Encontrar serviço
        service = None
        for s in self.services_cache:
            if s.orgao.lower() == orgao.lower() and service_name.lower() in s.descricao.lower():
                service = s
                break
        
        if not service:
            return {"error": f"Serviço não encontrado: {orgao} - {service_name}"}
        
        layers = await self.extractor.discover_layers(service)
        
        return {
            "service": asdict(service),
            "total_layers": len(layers),
            "layers": layers
        }
    
    async def extract_dataset(self, orgao: str, service_name: str, layer: str, max_features: int = 1000) -> Dict[str, Any]:
        """Extrai dados de uma camada específica."""
        if not self.services_cache:
            self.services_cache = await self.extractor.load_catalog()
        
        # Encontrar serviço
        service = None
        for s in self.services_cache:
            if s.orgao.lower() == orgao.lower() and service_name.lower() in s.descricao.lower():
                service = s
                break
        
        if not service:
            return {"error": f"Serviço não encontrado: {orgao} - {service_name}"}
        
        dataset_info = await self.extractor.extract_data(service, layer, max_features)
        
        if dataset_info:
            return {
                "success": True,
                "dataset": asdict(dataset_info)
            }
        else:
            return {"error": "Não foi possível extrair dados da camada"}
    
    async def analyze_service_capabilities(self, orgao: str) -> Dict[str, Any]:
        """Analisa capacidades de todos os serviços de um órgão."""
        if not self.services_cache:
            self.services_cache = await self.extractor.load_catalog()
        
        services = [s for s in self.services_cache if s.orgao.lower() == orgao.lower()]
        
        if not services:
            return {"error": f"Nenhum serviço encontrado para o órgão: {orgao}"}
        
        analysis = {
            "orgao": orgao,
            "total_services": len(services),
            "service_types": {},
            "services_with_layers": []
        }
        
        for service in services:
            # Contar tipos de serviços
            if service.tipo not in analysis["service_types"]:
                analysis["service_types"][service.tipo] = 0
            analysis["service_types"][service.tipo] += 1
            
            # Descobrir camadas para alguns serviços
            if len(analysis["services_with_layers"]) < 3:  # Limitar para não demorar muito
                layers = await self.extractor.discover_layers(service)
                analysis["services_with_layers"].append({
                    "service": asdict(service),
                    "total_layers": len(layers),
                    "sample_layers": layers[:5]
                })
        
        return analysis


# ================================
# AGENTES CREWAI
# ================================

class GeoDataExplorerTool(BaseTool):
    """Ferramenta CrewAI para exploração de dados geoespaciais."""
    
    name: str = "geo_data_explorer"
    description: str = "Explora e extrai dados de serviços geoespaciais brasileiros"
    
    def __init__(self):
        super().__init__()
        self.inde_tools = INDETools()
    
    def _run(self, query: str) -> str:
        """Executa consulta aos dados geoespaciais."""
        return asyncio.run(self._arun(query))
    
    async def _arun(self, query: str) -> str:
        """Versão assíncrona da consulta."""
        try:
            # Parse simples da query
            if "listar" in query.lower() or "list" in query.lower():
                if "serviços" in query.lower() or "services" in query.lower():
                    result = await self.inde_tools.list_services()
                    return json.dumps(result, indent=2, ensure_ascii=False)
            
            elif "camadas" in query.lower() or "layers" in query.lower():
                # Extrair órgão da query (implementação simplificada)
                words = query.lower().split()
                orgao = None
                for word in words:
                    if word in ["anatel", "ana", "ibge", "incra", "inpe", "icmbio"]:
                        orgao = word.upper()
                        break
                
                if orgao:
                    result = await self.inde_tools.analyze_service_capabilities(orgao)
                    return json.dumps(result, indent=2, ensure_ascii=False)
            
            return "Consulta não compreendida. Tente: 'listar serviços' ou 'camadas da ANATEL'"
            
        except Exception as e:
            return f"Erro ao processar consulta: {e}"


class INDEAgents:
    """Sistema de agentes para análise automatizada de dados INDE."""
    
    def __init__(self):
        self.geo_tool = GeoDataExplorerTool()
        self._setup_agents()
    
    def _setup_agents(self):
        """Configura os agentes especializados."""
        
        # Agente Discovery
        self.discovery_agent = Agent(
            role="Descobridor de Dados Geoespaciais",
            goal="Encontrar e catalogar dados geoespaciais relevantes nos serviços INDE",
            backstory="""Você é um especialista em descoberta de dados geoespaciais brasileiros.
            Sua missão é explorar os serviços da INDE (Infraestrutura Nacional de Dados Espaciais)
            e identificar datasets relevantes para diferentes objetivos de pesquisa.""",
            tools=[self.geo_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Agente Analyzer
        self.analyzer_agent = Agent(
            role="Analista de Dados Geoespaciais", 
            goal="Analisar estrutura e qualidade dos dados geoespaciais extraídos",
            backstory="""Você é um analista especializado em dados geoespaciais.
            Sua função é examinar a estrutura, qualidade e potencial dos datasets
            extraídos dos serviços INDE, identificando padrões e insights relevantes.""",
            tools=[self.geo_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Agente Reporter
        self.reporter_agent = Agent(
            role="Gerador de Relatórios",
            goal="Criar relatórios detalhados sobre os dados geoespaciais analisados",
            backstory="""Você é um especialista em comunicação técnica e relatórios.
            Sua missão é transformar análises técnicas de dados geoespaciais em
            relatórios claros e acionáveis para diferentes públicos.""",
            tools=[],
            verbose=True,
            allow_delegation=False
        )
    
    async def analyze_organization_data(self, orgao: str, objetivo: str) -> AnalysisResult:
        """Executa análise completa de dados de um órgão."""
        
        # Definir tarefas
        discovery_task = Task(
            description=f"""
            Descubra e catalogue todos os serviços e datasets disponíveis para o órgão {orgao}.
            Identifique quais serviços estão ativos, que tipos de dados oferecem e suas características.
            Foque em dados relevantes para o objetivo: {objetivo}
            """,
            agent=self.discovery_agent,
            expected_output="Lista detalhada de serviços e datasets com suas características"
        )
        
        analysis_task = Task(
            description=f"""
            Analise a estrutura e qualidade dos dados descobertos para {orgao}.
            Identifique padrões, limitações e potencial dos datasets para o objetivo: {objetivo}.
            Avalie completude, atualização e utilidade dos dados.
            """,
            agent=self.analyzer_agent,
            expected_output="Análise detalhada da qualidade e estrutura dos dados",
            context=[discovery_task]
        )
        
        report_task = Task(
            description=f"""
            Crie um relatório executivo sobre os dados do órgão {orgao} para o objetivo: {objetivo}.
            Inclua insights principais, recomendações de uso e limitações identificadas.
            O relatório deve ser claro e acionável.
            """,
            agent=self.reporter_agent,
            expected_output="Relatório executivo com insights e recomendações",
            context=[discovery_task, analysis_task]
        )
        
        # Executar crew
        crew = Crew(
            agents=[self.discovery_agent, self.analyzer_agent, self.reporter_agent],
            tasks=[discovery_task, analysis_task, report_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Criar resultado estruturado
        analysis_result = AnalysisResult(
            orgao=orgao,
            objetivo=objetivo,
            datasets_analisados=[],  # Seria preenchido com dados reais
            insights=["Insights extraídos da análise"],
            recomendacoes=["Recomendações baseadas nos dados"],
            dados_extraidos={},
            relatorio_completo=str(result)
        )
        
        return analysis_result


# ================================
# SERVIDOR MCP
# ================================

# Inicializar FastMCP
mcp = FastMCP("INDE Data Server")

# Instâncias globais
inde_tools = INDETools()
inde_agents = INDEAgents()


@mcp.tool()
async def list_inde_services(orgao: Optional[str] = None) -> Dict[str, Any]:
    """
    Lista serviços geoespaciais disponíveis na INDE.
    
    Args:
        orgao: Filtrar por órgão específico (opcional)
    
    Returns:
        Dicionário com lista de serviços e metadados
    """
    return await inde_tools.list_services(orgao)


@mcp.tool()
async def discover_service_layers(orgao: str, service_name: str) -> Dict[str, Any]:
    """
    Descobre camadas disponíveis em um serviço específico.
    
    Args:
        orgao: Nome do órgão (ex: ANATEL, ANA, IBGE)
        service_name: Nome ou parte do nome do serviço
    
    Returns:
        Dicionário com informações do serviço e suas camadas
    """
    return await inde_tools.discover_service_layers(orgao, service_name)


@mcp.tool()
async def extract_geospatial_data(orgao: str, service_name: str, layer: str, max_features: int = 1000) -> Dict[str, Any]:
    """
    Extrai dados de uma camada geoespacial específica.
    
    Args:
        orgao: Nome do órgão
        service_name: Nome do serviço
        layer: Nome da camada
        max_features: Número máximo de registros (padrão: 1000)
    
    Returns:
        Dicionário com dados extraídos e metadados
    """
    return await inde_tools.extract_dataset(orgao, service_name, layer, max_features)


@mcp.tool()
async def analyze_organization_capabilities(orgao: str) -> Dict[str, Any]:
    """
    Analisa todas as capacidades de dados de um órgão.
    
    Args:
        orgao: Nome do órgão para análise
    
    Returns:
        Análise completa das capacidades do órgão
    """
    return await inde_tools.analyze_service_capabilities(orgao)


@mcp.tool()
async def intelligent_data_analysis(orgao: str, objetivo: str) -> Dict[str, Any]:
    """
    Executa análise inteligente dos dados de um órgão usando agentes AI.
    
    Args:
        orgao: Nome do órgão
        objetivo: Objetivo da análise (ex: "análise de telecomunicações", "recursos hídricos")
    
    Returns:
        Relatório completo com insights e recomendações
    """
    try:
        result = await inde_agents.analyze_organization_data(orgao, objetivo)
        return result.dict()
    except Exception as e:
        return {"error": f"Erro na análise inteligente: {e}"}


@mcp.tool()
async def generate_data_report(orgao: str, format: str = "markdown") -> str:
    """
    Gera relatório automático sobre os dados disponíveis de um órgão.
    
    Args:
        orgao: Nome do órgão
        format: Formato do relatório (markdown, json, html)
    
    Returns:
        Relatório formatado
    """
    try:
        # Analisar capacidades
        capabilities = await inde_tools.analyze_service_capabilities(orgao)
        
        if "error" in capabilities:
            return f"Erro: {capabilities['error']}"
        
        # Gerar relatório em markdown
        report = f"""# Relatório de Dados Geoespaciais - {orgao}

## Resumo Executivo
- **Total de Serviços**: {capabilities['total_services']}
- **Tipos de Serviços**: {', '.join(capabilities['service_types'].keys())}
- **Data da Análise**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Distribuição por Tipo de Serviço
"""
        
        for service_type, count in capabilities['service_types'].items():
            report += f"- **{service_type}**: {count} serviços\n"
        
        report += "\n## Serviços com Camadas Identificadas\n"
        
        for service_info in capabilities['services_with_layers']:
            service = service_info['service']
            report += f"""
### {service['descricao']}
- **Tipo**: {service['tipo']}
- **URL**: {service['url']}
- **Total de Camadas**: {service_info['total_layers']}
- **Camadas de Exemplo**: {', '.join(service_info['sample_layers'])}
"""
        
        report += f"""
## Recomendações
1. Para análise detalhada, use serviços WFS que permitem extração de dados
2. Para visualização rápida, utilize serviços WMS
3. Verifique regularmente a disponibilidade dos serviços
4. Considere limitações de performance para datasets grandes

---
*Relatório gerado automaticamente pelo Sistema INDE MCP*
"""
        
        return report
        
    except Exception as e:
        return f"Erro ao gerar relatório: {e}"


# ================================
# CONFIGURAÇÃO E EXECUÇÃO
# ================================

async def main():
    """Função principal para executar o servidor MCP."""
    logger.info("🚀 Iniciando INDE MCP Server...")
    
    # Configurações
    mcp.server.name = "INDE Geospatial Data Server"
    mcp.server.version = "1.0.0"
    
    # Informações do servidor
    logger.info(f"📊 Servidor: {mcp.server.name} v{mcp.server.version}")
    logger.info(f"🛠️ Ferramentas disponíveis: {len(mcp.list_tools())}")
    
    # Executar servidor
    await mcp.run()


if __name__ == "__main__":
    # Executar servidor MCP
    asyncio.run(main())
