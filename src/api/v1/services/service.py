from uuid import UUID, uuid4

from fastapi import status

from api.v1.services.proxies import RetrieveServiceSchema, ServiceProxy
from api.v1.services.schemas import CreateServiceSchema, ListServiceSchema
from core.settings import settings
from core.utils.encryted import EncryptedController
from core.utils.exceptions import FormException
from core.utils.generic_views import (
    BaseService,
    ListBaseService,
    ObjectBaseService,
)
from core.utils.responses import create_simple_envelope_response


class CreateServicesService(BaseService):
    model = ServiceProxy
    schema = RetrieveServiceSchema

    def _validate_request(self, payload: CreateServiceSchema):  # noqa: ARG002
        success_request = True

        # TODO make validations  # noqa: TD004

        if self.request_errors["validations_success"] is False:
            raise FormException(field_errors=self.request_errors["validations_errors"])
        return success_request

    def create(self, payload: CreateServiceSchema):
        self.request_errors = {"validations_errors": {}, "validations_success": True}
        self._validate_request(payload=payload)

        new_uuid = uuid4()

        encrypted_controller = EncryptedController(key=settings.ROOT_ENCRYPTED_KEY)

        api_key = encrypted_controller.encrypt(new_uuid.__str__())

        instance = self.model(**payload.model_dump(), api_key=api_key)
        self.session.add(instance)
        self.session.commit()

        instance.api_key = new_uuid

        return create_simple_envelope_response(
            data=instance.dict(),
            message="Service Created successfully",
            status_code=status.HTTP_201_CREATED,
            successful=True,
        )


class ListServicesService(ListBaseService):
    model = ServiceProxy
    schema = ListServiceSchema


class RetrieveServicesService(ObjectBaseService):
    model = ServiceProxy
    schema = RetrieveServiceSchema

    def retrieve(self, id: UUID):
        instance = self.get_object(id)
        encrypted_controller = EncryptedController(key=settings.ROOT_ENCRYPTED_KEY)

        instance.api_key = encrypted_controller.decrypt(instance.api_key)

        return create_simple_envelope_response(
            data=instance.dict(),
            message="Retrive Service",
            status_code=status.HTTP_200_OK,
            successful=True,
        )
