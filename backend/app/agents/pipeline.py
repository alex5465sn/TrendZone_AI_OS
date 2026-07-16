"""
TrendZone AI OS
================================

Pipeline.

Define a sequência oficial
de execução dos Agents.

O Orchestrator nunca deverá
conhecer diretamente os Agents.

Ele apenas executa este Pipeline.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class PipelineStep:

    agent_id: str

    enabled: bool = True


class Pipeline:

    def __init__(self):

        self.steps: list[PipelineStep] = []

    # =====================================================
    # CONFIGURAÇÃO
    # =====================================================

    def add(self, agent_id: str):

        self.steps.append(

            PipelineStep(agent_id)

        )

        return self

    def disable(self, agent_id: str):

        for step in self.steps:

            if step.agent_id == agent_id:

                step.enabled = False

    def enable(self, agent_id: str):

        for step in self.steps:

            if step.agent_id == agent_id:

                step.enabled = True

    # =====================================================
    # CONSULTAS
    # =====================================================

    def get_steps(self):

        return [

            step

            for step in self.steps

            if step.enabled

        ]

    def names(self):

        return [

            step.agent_id

            for step in self.get_steps()

        ]

    def clear(self):

        self.steps.clear()

    def __len__(self):

        return len(self.steps)