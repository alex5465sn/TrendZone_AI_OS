"""
TrendZone AI OS
================================

Pacote oficial de Agents.

Todos os Agents devem ser
importados por este módulo.

Nunca importe diretamente
os arquivos individuais.
"""

from app.agents.base_agent import BaseAgent
from app.agents.context import AgentContext
from app.agents.result import AgentResult

from app.agents.registry import AgentRegistry
from app.agents.factory import AgentFactory

from app.agents.pipeline import Pipeline
from app.agents.default_pipeline import pipeline

from app.agents.orchestrator import Orchestrator

from app.agents.scout_agent import ScoutAgent
from app.agents.analyst_agent import AnalystAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.ceo_agent import CEOAgent
from app.agents.publisher_agent import PublisherAgent


#
# Registro automático dos Agents
#

AgentRegistry.register(ScoutAgent)
AgentRegistry.register(AnalystAgent)
AgentRegistry.register(RankingAgent)
AgentRegistry.register(CEOAgent)
AgentRegistry.register(PublisherAgent)


__all__ = [

    "BaseAgent",

    "AgentContext",

    "AgentResult",

    "AgentRegistry",

    "AgentFactory",

    "Pipeline",

    "pipeline",

    "Orchestrator",

    "ScoutAgent",

    "AnalystAgent",

    "RankingAgent",

    "CEOAgent",

    "PublisherAgent",

]