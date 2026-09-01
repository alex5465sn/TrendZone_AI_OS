from pydantic import BaseModel


class ReportFilters(BaseModel):

    purchaseTimeStart: int | None = None

    purchaseTimeEnd: int | None = None

    completeTimeStart: int | None = None

    completeTimeEnd: int | None = None

    orderStatus: str = "ALL"

    buyerType: str = "ALL"

    productType: str = "ALL"

    fraudStatus: str = "ALL"

    device: str = "ALL"

    limit: int = 20

    scrollId: str | None = None