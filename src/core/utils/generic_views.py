import datetime
import decimal
import logging
from urllib.parse import parse_qs, urlencode, urlparse
from uuid import UUID

from fastapi import Request, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import JSON, DateTime, Select, select, types
from sqlalchemy.dialects.postgresql import JSON as PJSON
from sqlalchemy.orm import DeclarativeBase, Session

from core.utils.exceptions import NoResultFound
from core.utils.filters import ManagerFilter
from core.utils.orm import Manager, QueryModel
from core.utils.responses import PaginationParams, create_envelope_response
from core.utils.schema_base import BaseSchema

logger = logging.getLogger(__name__)


class Base(DeclarativeBase, QueryModel):
    session: Session
    objects = Manager["Base"]()

    type_annotation_map = {  # noqa: RUF012
        datetime.date: types.Date(),
        datetime.datetime: types.DateTime(timezone=True),
        DateTime: types.DateTime(timezone=True),
        decimal.Decimal: types.Numeric(19, 2),
        JSON: PJSON,
    }

    def __repr__(self) -> str:
        return self.__str__()


class BaseService:
    model: Base
    schema: BaseSchema = BaseSchema
    envelop_response = create_envelope_response

    def __init__(self, session: Session):
        self.session = session

    def get_queryset(
        self,
        unary_expressions: list | None = None,
        filters: dict | None = None,
        order_by: list | None = None,
    ):
        if order_by is None:
            order_by = []
        if filters is None:
            filters = {}
        if unary_expressions is None:
            unary_expressions = []

        return select(self.model).where(*unary_expressions).filter_by(**filters).order_by(*order_by)

    def get_ordered_queryset(self, filters: dict):
        unary_expressions, filters, order_by = ManagerFilter(model=self.model, filters=filters).manage_filters()
        return self.get_queryset(unary_expressions=unary_expressions, filters=filters, order_by=order_by)

    def get_query(self, filters: dict):
        return self.get_ordered_queryset(filters)

    def get_objects(self, filters: dict) -> list:
        query = self.get_query(filters)
        return self.session.execute(query).scalars().all()

    def transform_to_schema(self, instance: Base):
        return self.schema(**instance.dict())

    def create_response(self, data, links=None, count=None):
        return create_envelope_response(data=data, links=links, count=count)


class ObjectBaseService(BaseService):
    def get_object(self, id: UUID):
        instance = self.session.get(self.model, id)
        if not instance:
            message_error = f"There is no {self.model.__tablename__} with this ID: {id}"
            logger.warning(message_error)
            raise NoResultFound(message_error)
        return instance


class ListBaseService(BaseService):
    def _generate_pagination_links(self, current_page: int, page_size: int, total: int, request: Request):
        parsed_url = urlparse(str(request.url))
        params = parse_qs(parsed_url.query)
        total_pages = -(-total // page_size)

        # Calculate next page link
        next_page = None
        if current_page < total_pages:
            params["page"] = [current_page + 1]
            next_page = parsed_url._replace(query=urlencode(params, doseq=True)).geturl()

        # Calculate previous page link
        previous_page = None
        if current_page > 1:
            params["page"] = [current_page - 1]
            previous_page = parsed_url._replace(query=urlencode(params, doseq=True)).geturl()

        return next_page, previous_page

    def _apply_pagination(self, query: Select, pagination_params: PaginationParams) -> dict:
        page = paginate(self.session, query, pagination_params)
        return {"items": page.items, "total": page.total}

    def _build_response(self, next_link=None, prev_link=None, count=None, data=None):
        return {
            "links": {"next": next_link, "previous": prev_link},
            "count": count,
            "data": data,
        }

    def _process_list(self, filters: dict, pagination_params: PaginationParams, request: Request) -> dict:
        query = self.get_query(filters)
        page_info = self._apply_pagination(query, pagination_params)

        # Transform each item to its schema
        data = [self.transform_to_schema(item) for item in page_info["items"]]
        total = page_info["total"]

        # Generate pagination links
        next_link, prev_link = self._generate_pagination_links(
            current_page=pagination_params.page,
            page_size=pagination_params.size,
            total=total,
            request=request,
        )
        return self._build_response(next_link, prev_link, total, data)

    def _process_all(self, filters: dict):
        results = self.get_objects(filters)
        data = [self.transform_to_schema(item) for item in results]
        return self._build_response(count=len(data), data=data)

    def list(self, filters: dict, pagination_params: PaginationParams, request: Request):
        if pagination_params.size <= 0:
            data = self._process_all(filters)
        else:
            data = self._process_list(filters, pagination_params, request)
        return create_envelope_response(
            **data,
            message="Retrive service",
            status_code=status.HTTP_200_OK,
            successful=True,
        )


def validation_group(validation_function):
    def wrapper(self, *args, **kwargs):
        result_validation_function = validation_function(self, *args, **kwargs)
        returns_validation_function_number = (
            len(result_validation_function) if type(result_validation_function) == tuple else 1
        )
        if returns_validation_function_number <= 1:
            errors = result_validation_function
            data = None
        elif returns_validation_function_number == 2:  # noqa: PLR2004
            errors, data = result_validation_function
        else:
            errors, *data = result_validation_function

        validations_success = not bool(len(errors))
        self.request_errors["validations_errors"].update(errors)
        self.request_errors["validations_success"] = (
            self.request_errors.get("validations_success", True) and validations_success
        )
        return validations_success, errors, data

    return wrapper
