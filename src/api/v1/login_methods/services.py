from uuid import UUID

from fastapi import status

from api.v1.codes.crud.schemas import CreateCodeSchema
from api.v1.login_methods.proxies import LoginMethodsProxy
from api.v1.login_methods.schemas import ListLoginMethodsSchema
from core.utils.generic_views import (
    BaseService,
    ListBaseService,
    ObjectBaseService,
)
from core.utils.repository_base import RepositoryBase
from core.utils.responses import create_simple_envelope_response


class ListLoginMethodService(ListBaseService):
    model = LoginMethodsProxy
    schema = ListLoginMethodsSchema


class RetrieveLoginMethodService(ObjectBaseService):
    model = LoginMethodsProxy
    schema = ListLoginMethodsSchema

    def retrieve(self, id: UUID):
        instance = self.get_object(id)

        return create_simple_envelope_response(
            data=instance.dict(),
            message="Retrive Code",
            status_code=status.HTTP_200_OK,
            successful=True,
        )


class CreateLoginMethodService(BaseService):
    model = LoginMethodsProxy
    schema = ListLoginMethodsSchema

    def _validate_request(self, payload: CreateCodeSchema):
        pass

    def create(self, payload: CreateCodeSchema):
        self.request_errors = {"validations_errors": {}, "validations_success": True}
        self._validate_request(payload=payload)

        instance = self.model(**payload.model_dump())
        self.session.add(instance)
        self.session.commit()

        return create_simple_envelope_response(
            data=instance.dict(),
            message="Login Method Created successfully",
            status_code=status.HTTP_201_CREATED,
            successful=True,
        )


class DeleteLoginMethodService(RepositoryBase):
    model = LoginMethodsProxy
    schema = ListLoginMethodsSchema

    def delete(self, id: UUID):
        self.delete_by_id(id=id)

        return create_simple_envelope_response(
            data=None,
            message="Delete Login Methods",
            status_code=status.HTTP_200_OK,
            successful=True,
        )
