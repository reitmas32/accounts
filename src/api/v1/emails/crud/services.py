from uuid import UUID

from fastapi import status

from api.v1.emails.crud.proxies import EmailProxy
from api.v1.emails.crud.schemas import CreateEmailSchema, ListEmailSchema
from core.utils.generic_views import (
    BaseService,
    ListBaseService,
    ObjectBaseService,
)
from core.utils.repository_base import RepositoryBase
from core.utils.responses import (
    create_simple_envelope_response,
)
from shared.app.handlers.password import PasswordHandler


class ListEmailsService(ListBaseService):
    model = EmailProxy
    schema = ListEmailSchema


class RetrieveEmailsService(ObjectBaseService):
    model = EmailProxy
    schema = ListEmailSchema

    def retrieve(self, id: UUID):
        instance = self.get_object(id)

        data: dict = instance.dict()
        data.pop("password")
        return create_simple_envelope_response(
            data=data,
            message="Retrive Email",
            status_code=status.HTTP_200_OK,
            successful=True,
        )


class CreateEmailsService(BaseService):
    model = EmailProxy
    schema = ListEmailSchema

    def _validate_request(self, payload: CreateEmailSchema):
        pass

    def create(self, payload: CreateEmailSchema):
        self.request_errors = {"validations_errors": {}, "validations_success": True}
        self._validate_request(payload=payload)

        payload.password = PasswordHandler.hash_password(password=payload.password)

        instance = self.model(**payload.model_dump())
        self.session.add(instance)
        self.session.commit()

        data: dict = instance.dict()
        data.pop("password")

        return create_simple_envelope_response(
            data=data,
            message="Email Created successfully",
            status_code=status.HTTP_201_CREATED,
            successful=True,
        )


class DeleteEmailsService(RepositoryBase):
    model = EmailProxy
    schema = ListEmailSchema

    def delete(self, id: UUID):
        self.delete_by_id(id=id)

        return create_simple_envelope_response(
            data=None,
            message="Delete Code",
            status_code=status.HTTP_200_OK,
            successful=True,
        )
