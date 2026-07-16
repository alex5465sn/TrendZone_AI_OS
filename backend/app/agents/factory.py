"""
TrendZone AI OS
================================

Agent Factory.

Responsável por criar instâncias
dos Agents registrados.

Nenhuma classe do sistema deverá
instanciar Agents diretamente.

Sempre utilize AgentFactory.
"""

from app.agents.registry import AgentRegistry
from app.core.exceptions import TrendZoneException


class AgentFactory:

    @staticmethod
    def create(agent_name: str):

        agent_class = AgentRegistry.get(agent_name)

        if agent_class is None:

            raise TrendZoneException(
                f"Agent '{agent_name}' não encontrado."
            )

        return agent_class()

    @staticmethod
    def create_many(agent_names: list[str]):

        agents = []

        for name in agent_names:

            agents.append(

                AgentFactory.create(name)

            )

        return agents