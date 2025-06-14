#!/usr/bin/env python3
"""
Sistema de Monitoramento - INDE MCP Server
Monitoramento completo, métricas e alertas para o sistema MCP

Funcionalidades:
- Monitoramento de saúde dos serviços
- Métricas de performance
- Sistema de alertas
- Dashboard de métricas
- Logs estruturados
"""

import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import aiohttp
import psutil
from collections import defaultdict, deque

# Prometheus metrics (opcional)
try:
    from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

# ================================
# MODELOS DE DADOS
# ================================

@dataclass
class ServiceHealth:
    """Status de saúde de um serviço."""
    name: str
    url: str
    status: str  # "healthy", "degraded", "unhealthy"
    response_time: float
    last_check: datetime
    error_message: Optional[str] = None
    uptime_percentage: float = 0.0

@dataclass
class PerformanceMetrics:
    """Métricas de performance do sistema."""
    timestamp: datetime
    requests_total: int
    requests_per_second: float
    avg_response_time: float
    error_rate: float
    cache_hit_rate: float
    memory_usage: float
    cpu_usage: float
    active_connections: int

@dataclass
class Alert:
    """Alerta do sistema."""
    id: str
    level: str  # "info", "warning", "critical"
    message: str
    service: str
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None

# ================================
# SISTEMA DE MÉTRICAS
# ================================

class MetricsCollector:
    """Coletor de métricas do sistema."""
    
    def __init__(self):
        self.metrics_history = deque(maxlen=1000)
        self.service_stats = defaultdict(lambda: {
            'requests': 0,
            'errors': 0,
            'total_time': 0.0,
            'last_request': None
        })
        
        # Métricas Prometheus (se disponível)
        if PROMETHEUS_AVAILABLE:
            self.registry = CollectorRegistry()
            self._setup_prometheus_metrics()
        
        # Contadores internos
        self.start_time = datetime.now()
        self.total_requests = 0
        self.total_errors = 0
    
    def _setup_prometheus_metrics(self):
        """Configura métricas Prometheus."""
        self.request_counter = Counter(
            'inde_mcp_requests_total',
            'Total number of requests',
            ['service', 'method', 'status'],
            registry=self.registry
        )
        
        self.request_duration = Histogram(
            'inde_mcp_request_duration_seconds',
            'Request duration in seconds',
            ['service', 'method'],
            registry=self.registry
        )
        
        self.active_connections = Gauge(
            'inde_mcp_active_connections',
            'Number of active connections',
            registry=self.registry
        )
        
        self.memory_usage = Gauge(
            'inde_mcp_memory_usage_bytes',
            'Memory usage in bytes',
            registry=self.registry
        )
        
        self.cpu_usage = Gauge(
            'inde_mcp_cpu_usage_percent',
            'CPU usage percentage',
            registry=self.registry
        )
    
    def record_request(self, service: str, method: str, duration: float, status: str = "success"):
        """Registra uma requisição."""
        self.total_requests += 1
        
        if status == "error":
            self.total_errors += 1
        
        # Atualizar estatísticas do serviço
        stats = self.service_stats[service]
        stats['requests'] += 1
        stats['total_time'] += duration
        stats['last_request'] = datetime.now()
        
        if status == "error":
            stats['errors'] += 1
        
        # Prometheus
        if PROMETHEUS_AVAILABLE:
            self.request_counter.labels(service=service, method=method, status=status).inc()
            self.request_duration.labels(service=service, method=method).observe(duration)
    
    def get_current_metrics(self) -> PerformanceMetrics:
        """Obtém métricas atuais do sistema."""
        now = datetime.now()
        uptime = (now - self.start_time).total_seconds()
        
        # Calcular RPS (últimos 60 segundos)
        recent_requests = sum(
            1 for service_stats in self.service_stats.values()
            if service_stats['last_request'] and 
            (now - service_stats['last_request']).total_seconds() < 60
        )
        
        rps = recent_requests / min(60, uptime) if uptime > 0 else 0
        
        # Calcular tempo médio de resposta
        total_time = sum(stats['total_time'] for stats in self.service_stats.values())
        avg_response_time = total_time / self.total_requests if self.total_requests > 0 else 0
        
        # Taxa de erro
        error_rate = (self.total_errors / self.total_requests * 100) if self.total_requests > 0 else 0
        
        # Métricas do sistema
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        cpu_usage = process.cpu_percent()
        
        metrics = PerformanceMetrics(
            timestamp=now,
            requests_total=self.total_requests,
            requests_per_second=rps,
            avg_response_time=avg_response_time,
            error_rate=error_rate,
            cache_hit_rate=0.0,  # Implementar cache metrics
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            active_connections=0  # Implementar connection tracking
        )
        
        # Atualizar Prometheus
        if PROMETHEUS_AVAILABLE:
            self.memory_usage.set(memory_usage * 1024 * 1024)  # Bytes
            self.cpu_usage.set(cpu_usage)
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_service_stats(self, service: str) -> Dict[str, Any]:
        """Obtém estatísticas de um serviço específico."""
        stats = self.service_stats[service]
        
        avg_response_time = (
            stats['total_time'] / stats['requests'] 
            if stats['requests'] > 0 else 0
        )
        
        error_rate = (
            stats['errors'] / stats['requests'] * 100
            if stats['requests'] > 0 else 0
        )
        
        return {
            'requests': stats['requests'],
            'errors': stats['errors'],
            'error_rate': error_rate,
            'avg_response_time': avg_response_time,
            'last_request': stats['last_request']
        }
    
    def export_prometheus_metrics(self) -> str:
        """Exporta métricas no formato Prometheus."""
        if not PROMETHEUS_AVAILABLE:
            return "# Prometheus not available\n"
        
        return generate_latest(self.registry).decode('utf-8')


# ================================
# MONITOR DE SAÚDE DOS SERVIÇOS
# ================================

class ServiceHealthMonitor:
    """Monitor de saúde dos serviços INDE."""
    
    def __init__(self, check_interval: int = 300):  # 5 minutos
        self.check_interval = check_interval
        self.services = {}
        self.health_history = defaultdict(list)
        self.running = False
    
    def add_service(self, name: str, url: str, check_function: Optional[Callable] = None):
        """Adiciona um serviço para monitoramento."""
        self.services[name] = {
            'url': url,
            'check_function': check_function or self._default_health_check,
            'last_health': None
        }
    
    async def _default_health_check(self, url: str) -> tuple[str, float, Optional[str]]:
        """Check de saúde padrão via HTTP."""
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    duration = time.time() - start_time
                    
                    if response.status == 200:
                        return "healthy", duration, None
                    else:
                        return "degraded", duration, f"HTTP {response.status}"
                        
        except asyncio.TimeoutError:
            return "unhealthy", 30.0, "Timeout"
        except Exception as e:
            return "unhealthy", 30.0, str(e)
    
    async def check_service_health(self, name: str) -> ServiceHealth:
        """Verifica saúde de um serviço específico."""
        service_info = self.services[name]
        
        status, response_time, error_message = await service_info['check_function'](
            service_info['url']
        )
        
        # Calcular uptime
        history = self.health_history[name]
        healthy_checks = sum(1 for h in history[-100:] if h.status == "healthy")
        uptime_percentage = (healthy_checks / len(history[-100:])) * 100 if history else 0
        
        health = ServiceHealth(
            name=name,
            url=service_info['url'],
            status=status,
            response_time=response_time,
            last_check=datetime.now(),
            error_message=error_message,
            uptime_percentage=uptime_percentage
        )
        
        self.services[name]['last_health'] = health
        self.health_history[name].append(health)
        
        return health
    
    async def check_all_services(self) -> Dict[str, ServiceHealth]:
        """Verifica saúde de todos os serviços."""
        results = {}
        
        tasks = [
            self.check_service_health(name)
            for name in self.services.keys()
        ]
        
        health_checks = await asyncio.gather(*tasks, return_exceptions=True)
        
        for name, health in zip(self.services.keys(), health_checks):
            if isinstance(health, Exception):
                results[name] = ServiceHealth(
                    name=name,
                    url=self.services[name]['url'],
                    status="unhealthy",
                    response_time=0.0,
                    last_check=datetime.now(),
                    error_message=str(health)
                )
            else:
                results[name] = health
        
        return results
    
    async def start_monitoring(self):
        """Inicia monitoramento contínuo."""
        self.running = True
        
        while self.running:
            try:
                await self.check_all_services()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logging.error(f"Erro no monitoramento: {e}")
                await asyncio.sleep(10)
    
    def stop_monitoring(self):
        """Para o monitoramento."""
        self.running = False


# ================================
# SISTEMA DE ALERTAS
# ================================

class AlertManager:
    """Gerenciador de alertas do sistema."""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules = []
        self.notification_handlers = []
    
    def add_alert_rule(self, rule: Callable[[Any], Optional[Alert]]):
        """Adiciona uma regra de alerta."""
        self.alert_rules.append(rule)
    
    def add_notification_handler(self, handler: Callable[[Alert], None]):
        """Adiciona um handler de notificação."""
        self.notification_handlers.append(handler)
    
    def check_alerts(self, metrics: PerformanceMetrics, health_status: Dict[str, ServiceHealth]):
        """Verifica se algum alerta deve ser disparado."""
        context = {
            'metrics': metrics,
            'health': health_status
        }
        
        for rule in self.alert_rules:
            try:
                alert = rule(context)
                if alert:
                    self._trigger_alert(alert)
            except Exception as e:
                logging.error(f"Erro ao verificar regra de alerta: {e}")
    
    def _trigger_alert(self, alert: Alert):
        """Dispara um alerta."""
        # Verificar se já existe alerta similar ativo
        existing = next(
            (a for a in self.alerts 
             if a.service == alert.service and a.level == alert.level and not a.resolved),
            None
        )
        
        if existing:
            return  # Alerta já existe
        
        self.alerts.append(alert)
        
        # Enviar notificações
        for handler in self.notification_handlers:
            try:
                handler(alert)
            except Exception as e:
                logging.error(f"Erro ao enviar notificação: {e}")
    
    def resolve_alert(self, alert_id: str):
        """Resolve um alerta."""
        for alert in self.alerts:
            if alert.id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                break
    
    def get_active_alerts(self) -> List[Alert]:
        """Retorna alertas ativos."""
        return [a for a in self.alerts if not a.resolved]


# ================================
# REGRAS DE ALERTA PADRÃO
# ================================

def create_default_alert_rules(alert_manager: AlertManager):
    """Cria regras de alerta padrão."""
    
    def high_error_rate_rule(context) -> Optional[Alert]:
        metrics = context['metrics']
        if metrics.error_rate > 10:  # >10% erro
            return Alert(
                id=f"high_error_rate_{int(time.time())}",
                level="critical",
                message=f"Alta taxa de erro: {metrics.error_rate:.1f}%",
                service="system",
                timestamp=datetime.now()
            )
        return None
    
    def slow_response_rule(context) -> Optional[Alert]:
        metrics = context['metrics']
        if metrics.avg_response_time > 10:  # >10s
            return Alert(
                id=f"slow_response_{int(time.time())}",
                level="warning",
                message=f"Resposta lenta: {metrics.avg_response_time:.1f}s",
                service="system",
                timestamp=datetime.now()
            )
        return None
    
    def service_down_rule(context) -> Optional[Alert]:
        health = context['health']
        for service_name, health_status in health.items():
            if health_status.status == "unhealthy":
                return Alert(
                    id=f"service_down_{service_name}_{int(time.time())}",
                    level="critical",
                    message=f"Serviço {service_name} indisponível: {health_status.error_message}",
                    service=service_name,
                    timestamp=datetime.now()
                )
        return None
    
    def high_memory_usage_rule(context) -> Optional[Alert]:
        metrics = context['metrics']
        if metrics.memory_usage > 1000:  # >1GB
            return Alert(
                id=f"high_memory_{int(time.time())}",
                level="warning",
                message=f"Alto uso de memória: {metrics.memory_usage:.1f}MB",
                service="system",
                timestamp=datetime.now()
            )
        return None
    
    # Adicionar regras ao manager
    alert_manager.add_alert_rule(high_error_rate_rule)
    alert_manager.add_alert_rule(slow_response_rule)
    alert_manager.add_alert_rule(service_down_rule)
    alert_manager.add_alert_rule(high_memory_usage_rule)


# ================================
# HANDLERS DE NOTIFICAÇÃO
# ================================

def console_notification_handler(alert: Alert):
    """Handler de notificação para console."""
    icon = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}[alert.level]
    print(f"{icon} [{alert.level.upper()}] {alert.service}: {alert.message}")

def log_notification_handler(alert: Alert):
    """Handler de notificação para logs."""
    level_map = {"info": logging.INFO, "warning": logging.WARNING, "critical": logging.CRITICAL}
    logging.log(level_map[alert.level], f"Alert: {alert.service} - {alert.message}")

async def webhook_notification_handler(alert: Alert, webhook_url: str):
    """Handler de notificação via webhook."""
    payload = {
        "alert_id": alert.id,
        "level": alert.level,
        "service": alert.service,
        "message": alert.message,
        "timestamp": alert.timestamp.isoformat()
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status != 200:
                    logging.error(f"Falha ao enviar webhook: {response.status}")
    except Exception as e:
        logging.error(f"Erro ao enviar webhook: {e}")


# ================================
# DASHBOARD DE MÉTRICAS
# ================================

class MetricsDashboard:
    """Dashboard simples para métricas."""
    
    def __init__(self, metrics_collector: MetricsCollector, 
                 health_monitor: ServiceHealthMonitor,
                 alert_manager: AlertManager):
        self.metrics = metrics_collector
        self.health = health_monitor
        self.alerts = alert_manager
    
    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Gera dados para o dashboard."""
        current_metrics = self.metrics.get_current_metrics()
        
        # Status dos serviços
        service_status = {}
        for name, service_info in self.health.services.items():
            if service_info['last_health']:
                service_status[name] = asdict(service_info['last_health'])
        
        # Alertas ativos
        active_alerts = [asdict(alert) for alert in self.alerts.get_active_alerts()]
        
        # Estatísticas por serviço
        service_stats = {}
        for service in self.health.services.keys():
            service_stats[service] = self.metrics.get_service_stats(service)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_metrics": asdict(current_metrics),
            "service_status": service_status,
            "service_stats": service_stats,
            "active_alerts": active_alerts,
            "total_services": len(self.health.services),
            "healthy_services": sum(
                1 for status in service_status.values()
                if status.get('status') == 'healthy'
            )
        }
    
    def generate_html_dashboard(self) -> str:
        """Gera dashboard HTML simples."""
        data = self.generate_dashboard_data()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>INDE MCP - Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; border: 1px solid #ddd; }}
        .healthy {{ color: green; }}
        .warning {{ color: orange; }}
        .critical {{ color: red; }}
        .alert {{ padding: 10px; margin: 5px; border-left: 4px solid red; background: #ffe6e6; }}
    </style>
</head>
<body>
    <h1>🚀 INDE MCP Server - Dashboard</h1>
    <p>Última atualização: {data['timestamp']}</p>
    
    <h2>📊 Métricas do Sistema</h2>
    <div class="metric">
        <strong>Requisições Totais:</strong> {data['system_metrics']['requests_total']}
    </div>
    <div class="metric">
        <strong>RPS:</strong> {data['system_metrics']['requests_per_second']:.1f}
    </div>
    <div class="metric">
        <strong>Tempo Médio:</strong> {data['system_metrics']['avg_response_time']:.1f}s
    </div>
    <div class="metric">
        <strong>Taxa de Erro:</strong> {data['system_metrics']['error_rate']:.1f}%
    </div>
    <div class="metric">
        <strong>Memória:</strong> {data['system_metrics']['memory_usage']:.1f}MB
    </div>
    <div class="metric">
        <strong>CPU:</strong> {data['system_metrics']['cpu_usage']:.1f}%
    </div>
    
    <h2>🏥 Status dos Serviços</h2>
    <p>Serviços saudáveis: {data['healthy_services']}/{data['total_services']}</p>
    """
        
        for service, status in data['service_status'].items():
            status_class = status['status']
            html += f"""
    <div class="metric {status_class}">
        <strong>{service}:</strong> {status['status']} 
        ({status['response_time']:.1f}s, {status['uptime_percentage']:.1f}% uptime)
    </div>
            """
        
        if data['active_alerts']:
            html += "<h2>🚨 Alertas Ativos</h2>"
            for alert in data['active_alerts']:
                html += f"""
    <div class="alert">
        <strong>[{alert['level'].upper()}]</strong> {alert['service']}: {alert['message']}
        <br><small>{alert['timestamp']}</small>
    </div>
                """
        
        html += """
    <h2>📈 Estatísticas por Serviço</h2>
    <table border="1">
        <tr><th>Serviço</th><th>Requisições</th><th>Erros</th><th>Taxa Erro</th><th>Tempo Médio</th></tr>
        """
        
        for service, stats in data['service_stats'].items():
            html += f"""
        <tr>
            <td>{service}</td>
            <td>{stats['requests']}</td>
            <td>{stats['errors']}</td>
            <td>{stats['error_rate']:.1f}%</td>
            <td>{stats['avg_response_time']:.1f}s</td>
        </tr>
            """
        
        html += """
    </table>
</body>
</html>
        """
        
        return html


# ================================
# SISTEMA PRINCIPAL DE MONITORAMENTO
# ================================

class INDEMonitoringSystem:
    """Sistema principal de monitoramento."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.health_monitor = ServiceHealthMonitor()
        self.alert_manager = AlertManager()
        self.dashboard = MetricsDashboard(
            self.metrics_collector,
            self.health_monitor, 
            self.alert_manager
        )
        
        # Configurar alertas padrão
        create_default_alert_rules(self.alert_manager)
        
        # Configurar notificações
        self.alert_manager.add_notification_handler(console_notification_handler)
        self.alert_manager.add_notification_handler(log_notification_handler)
    
    def setup_default_services(self):
        """Configura serviços padrão para monitoramento."""
        default_services = [
            ("ANATEL", "https://sistemas.anatel.gov.br/geoserver/ows"),
            ("ANA", "https://metadados.snirh.gov.br/geoserver/wfs"),
            ("IBGE", "https://geoservicos.ibge.gov.br/geoserver/wfs"),
            ("INCRA", "https://certificacao.incra.gov.br/csv_shp/export_shp.py"),
            ("ICMBio", "https://geoservicos.icmbio.gov.br/geoserver/ows")
        ]
        
        for name, url in default_services:
            self.health_monitor.add_service(name, url)
    
    async def start(self):
        """Inicia o sistema de monitoramento."""
        logging.info("🚀 Iniciando sistema de monitoramento INDE MCP")
        
        # Setup serviços padrão
        self.setup_default_services()
        
        # Iniciar monitoramento de saúde
        health_task = asyncio.create_task(self.health_monitor.start_monitoring())
        
        # Loop principal de monitoramento
        while True:
            try:
                # Coletar métricas
                metrics = self.metrics_collector.get_current_metrics()
                
                # Verificar saúde dos serviços
                health_status = await self.health_monitor.check_all_services()
                
                # Verificar alertas
                self.alert_manager.check_alerts(metrics, health_status)
                
                # Log de status
                healthy_count = sum(1 for h in health_status.values() if h.status == "healthy")
                total_count = len(health_status)
                
                logging.info(
                    f"📊 Status: {healthy_count}/{total_count} serviços saudáveis, "
                    f"{metrics.requests_per_second:.1f} RPS, "
                    f"{metrics.error_rate:.1f}% erro, "
                    f"{metrics.memory_usage:.1f}MB RAM"
                )
                
                # Aguardar próximo ciclo
                await asyncio.sleep(60)  # Verificar a cada minuto
                
            except Exception as e:
                logging.error(f"Erro no loop de monitoramento: {e}")
                await asyncio.sleep(10)
    
    def get_health_endpoint(self) -> Dict[str, Any]:
        """Endpoint de saúde para load balancers."""
        metrics = self.metrics_collector.get_current_metrics()
        
        # Sistema é saudável se:
        # - Taxa de erro < 20%
        # - Tempo de resposta < 30s
        # - Uso de memória < 2GB
        
        is_healthy = (
            metrics.error_rate < 20 and
            metrics.avg_response_time < 30 and
            metrics.memory_usage < 2000
        )
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "metrics": asdict(metrics)
        }
    
    def get_metrics_endpoint(self) -> str:
        """Endpoint de métricas para Prometheus."""
        return self.metrics_collector.export_prometheus_metrics()


# ================================
# EXEMPLO DE USO
# ================================

async def main():
    """Exemplo de uso do sistema de monitoramento."""
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Criar sistema de monitoramento
    monitoring = INDEMonitoringSystem()
    
    # Simular algumas requisições para teste
    for i in range(10):
        monitoring.metrics_collector.record_request(
            "ANATEL", "list_services", 
            1.5, "success" if i < 8 else "error"
        )
    
    # Executar uma verificação manual
    await monitoring.health_monitor.check_all_services()
    
    # Gerar dashboard
    dashboard_html = monitoring.dashboard.generate_html_dashboard()
    
    # Salvar dashboard
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    
    print("✅ Dashboard salvo em: dashboard.html")
    print("📊 Métricas disponíveis via API")
    print("🏥 Health check configurado")
    
    # Para uso real, descomente a linha abaixo para iniciar monitoramento contínuo
    # await monitoring.start()


if __name__ == "__main__":
    asyncio.run(main())
