from uuid import uuid4


def new_execution_id() -> str:

    return uuid4().hex[:8].upper()