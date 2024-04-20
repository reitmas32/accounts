from uuid import UUID, uuid4

from fastapi import status

from api.v1.codes.proxies import CodeProxy
from api.v1.codes.schemas import CreateCodeSchema, ListCodeSchema
from core.utils.generic_views import (
    BaseService,
    ListBaseService,
    ObjectBaseService,
)
from core.utils.repository_base import RepositoryBase
from core.utils.responses import create_simple_envelope_response
from models.enum import CodeTypeEnum, UserLoginMethodsTypeEnum


class ListCodesService(ListBaseService):
    model = CodeProxy
    schema = ListCodeSchema


class RetrieveCodesService(ObjectBaseService):
    model = CodeProxy
    schema = ListCodeSchema

    def retrieve(self, id: UUID):
        instance = self.get_object(id)

        return create_simple_envelope_response(
            data=instance.dict(),
            message="Retrive Code",
            status_code=status.HTTP_200_OK,
            successful=True,
        )


class CreateCodesService(BaseService):
    model = CodeProxy
    schema = ListCodeSchema

    def _validate_request(self, payload: CreateCodeSchema):
        pass

    def create(self, payload: CreateCodeSchema):
        self.request_errors = {"validations_errors": {}, "validations_success": True}
        self._validate_request(payload=payload)

        new_uuid = uuid4()

        payload.entity_type = UserLoginMethodsTypeEnum.get_enum_from_str(payload.entity_type)
        payload.type = CodeTypeEnum.get_enum_from_str(payload.type)

        instance = self.model(**payload.model_dump())
        self.session.add(instance)
        self.session.commit()

        instance.api_key = new_uuid

        return create_simple_envelope_response(
            data=instance.dict(),
            message="Code Created successfully",
            status_code=status.HTTP_201_CREATED,
            successful=True,
        )


class DeleteCodesService(RepositoryBase):
    model = CodeProxy
    schema = ListCodeSchema

    def delete(self, id: UUID):
        self.delete_by_id(id=id)

        return create_simple_envelope_response(
            data=None,
            message="Delete Code",
            status_code=status.HTTP_200_OK,
            successful=True,
        )
