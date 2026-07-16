"""
TrendZone AI OS
================================

Agent Registry.

Responsável pelo registro e descoberta
dos agentes disponíveis no sistema.

Nunca instancie agentes diretamente
fora do Factory.
"""

from typing import Type

from app.agents.base_agent import BaseAgent


class AgentRegistry:

    _agents: dict[str, Type[BaseAgent]] = {}

    # =====================================================
    # REGISTRO
    # =====================================================

    @classmethod
    def register(cls, agent: Type[BaseAgent]):

        cls._agents[agent.NAME] = agent

    # =====================================================
    # CONSULTAS
    # =====================================================

    @classmethod
    def exists(cls, name: str) -> bool:

        return name in cls._agents

    @classmethod
    def get(cls, name: str):

        return cls._agents.get(name)

    @classmethod
    def all(cls):

        return cls._agents

    @classmethod
    def names(cls):

        return list(cls._agents.keys())

    @classmethod
    def clear(cls):

        cls._agents.clear()