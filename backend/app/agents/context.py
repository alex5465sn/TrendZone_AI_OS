"""
TrendZone AI OS
================================

Agent Context.

Objeto compartilhado entre todos
os Agents durante a execução
do Pipeline.

Todo Agent recebe um AgentContext.

Nunca passe dicionários soltos
entre Agents.
"""

from datetime import datetime
from uuid import uuid4


class AgentContext:

    def __init__(self):

        self.execution_id = str(uuid4())

        self.started_at = datetime.utcnow()

        self.finished_at = None

        self.current_agent = None

        self.products = []

        self.reports = []

        self.decisions = []

        self.metrics = {}

        self.metadata = {}

        self.errors = []

    # =====================================================
    # PRODUCTS
    # =====================================================

    def set_products(self, products):

        self.products = products

    def get_products(self):

        return self.products

    # =====================================================
    # REPORTS
    # =====================================================

    def add_report(self, report):

        self.reports.append(report)

    def set_reports(self, reports):

        self.reports = reports

    def get_reports(self):

        return self.reports

    # =====================================================
    # DECISIONS
    # =====================================================

    def add_decision(self, decision):

        self.decisions.append(decision)

    def get_decisions(self):

        return self.decisions

    # =====================================================
    # METRICS
    # =====================================================

    def set_metric(self, key, value):

        self.metrics[key] = value

    def get_metric(self, key):

        return self.metrics.get(key)

    # =====================================================
    # METADATA
    # =====================================================

    def set_metadata(self, key, value):

        self.metadata[key] = value

    def get_metadata(self, key):

        return self.metadata.get(key)

    # =====================================================
    # ERRORS
    # =====================================================

    def add_error(self, error):

        self.errors.append(error)

    # =====================================================
    # EXECUTION
    # =====================================================

    def finish(self):

        self.finished_at = datetime.utcnow()

    @property
    def duration(self):

        if not self.finished_at:

            return None

        return round(

            (

                self.finished_at

                - self.started_at

            ).total_seconds(),

            4,

        )