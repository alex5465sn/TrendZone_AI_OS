from enum import Enum


# ==========================================================
# Status do Sistema
# ==========================================================

class SystemStatus(str, Enum):

    ONLINE = "ONLINE"

    OFFLINE = "OFFLINE"

    STARTING = "STARTING"

    STOPPING = "STOPPING"


# ==========================================================
# Decisão da IA
# ==========================================================

class Decision(str, Enum):

    PROMOTE = "PROMOVER"

    TEST = "TESTAR"

    OBSERVE = "OBSERVAR"

    DISCARD = "DESCARTAR"


# ==========================================================
# Agentes
# ==========================================================

class Agent(str, Enum):

    SCOUT = "Scout"

    ANALYST = "Analyst"

    RANKING = "Ranking"

    CEO = "CEO"

    PUBLISHER = "Publisher"

    ORCHESTRATOR = "Orchestrator"


# ==========================================================
# Prioridade
# ==========================================================

class Priority(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


# ==========================================================
# Pipeline
# ==========================================================

class PipelineStage(str, Enum):

    SCOUT = "SCOUT"

    ANALYSIS = "ANALYSIS"

    RANKING = "RANKING"

    DECISION = "DECISION"

    PUBLICATION = "PUBLICATION"


# ==========================================================
# Score IA
# ==========================================================

MIN_SCORE_OBSERVE = 40

MIN_SCORE_TEST = 60

MIN_SCORE_PROMOTE = 80