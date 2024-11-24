from urllib.parse import parse_qs, urlencode

from starlette.datastructures import URL

from shared.app.entities.list_body import ListBodyEntity
from shared.databases.infrastructure.repository import RepositoryInterface
from shared.presentation.dtos.pagination_params import PaginationParams


class ListBaseUseCase:
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, filters: dict, pagination_params: PaginationParams, url: str):
        offset = (pagination_params.page - 1) * pagination_params.size

        entities = self.repository.get_by_attributes(
            filters=filters, offset=offset, limit=pagination_params.size
        )

        total = self.repository.lenght()

        next_link, prev_link = self._generate_pagination_links(
            current_page=pagination_params.page,
            page_size=pagination_params.size,
            total=total,
            url=url,
        )

        return ListBodyEntity(
            next=next_link, prev=prev_link, count=len(entities), results=entities
        )

    def _generate_pagination_links(
        self, current_page: int, page_size: int, total: int, url: URL
    ):
        params = parse_qs(url.query)
        total_pages = -(-total // page_size)

        # Calculate next page link
        next_page = None
        if current_page < total_pages:
            params["page"] = [current_page + 1]
            next_page = (
                f"{url.scheme}://{url.netloc}{url.path}?{urlencode(params, doseq=True)}"
            )

        # Calculate previous page link
        previous_page = None
        if current_page > 1:
            params["page"] = [current_page - 1]
            previous_page = (
                f"{url.scheme}://{url.netloc}{url.path}?{urlencode(params, doseq=True)}"
            )

        return next_page, previous_page
