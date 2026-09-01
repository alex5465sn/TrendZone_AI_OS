from dataclasses import dataclass


@dataclass
class ScrollPaginator:

    scroll_id: str | None = None

    def first_page(self) -> bool:

        return self.scroll_id is None

    def update(
        self,
        scroll_id: str | None,
    ):

        self.scroll_id = scroll_id

    def variables(
        self,
    ) -> dict:

        if self.scroll_id:

            return {
                "scrollId": self.scroll_id
            }

        return {}