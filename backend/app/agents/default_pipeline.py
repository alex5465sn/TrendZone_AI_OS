"""
Pipeline oficial do TrendZone AI OS.
"""

from app.agents.pipeline import Pipeline


pipeline = (

    Pipeline()

    .add("SCOUT")

    .add("ANALYST")

    .add("RANKING")

    .add("CEO")

    .add("PUBLISHER")

)