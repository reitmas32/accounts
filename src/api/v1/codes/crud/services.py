from datetime import datetime
from uuid import UUID, uuid4

from fastapi import status
from sqlalchemy import desc, select

from api.v1.codes.crud.proxies import CodeProxy
from api.v1.codes.crud.schemas import CreateCodeSchema, ListCodeSchema
from core.utils.generic_views import (
    BaseService,
    ListBaseService,
    ObjectBaseService,
)
from core.utils.repository_base import RepositoryBase
from core.utils.responses import create_simple_envelope_response
from models import (
    CodeModel,
)
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

class RepositoryCode(RepositoryBase):
    """
    Repository for operations related to verification codes.

    This repository provides methods for performing queries and operations on the CodeModel table.

    Args:
        RepositoryBase: Base class for repositories.

    Attributes:
        model: Model associated with the CodeModel table.

    Methods:
        get_code: Retrieves a verification code record associated with the given email, code, and minimum creation date.
    """

    model = CodeModel

    def get_code(self, entity_id: str, code: str, min_created: datetime) -> CodeModel:
        """
        Retrieves a verification code record associated with the given email, code, and minimum creation date.

        Args:
            email (str): Email associated with the verification code.
            code (str): Verification code.
            min_created (datetime): Minimum creation date for the verification code.

        Returns:
            CodeModel: Verification code record associated with the given parameters, or None if not found.
        """
        query = (
            select(CodeModel)
            .select_from(CodeModel)
            .where(
                CodeModel.entity_id == entity_id,
                CodeModel.code == code,
                CodeModel.used_at is None,
                CodeModel.created >= min_created,
            )
            .order_by(desc(self.model.created))
        )
        result = self.session.execute(query).one_or_none()
        return result[0] if result else None

    def get_code_by_user_id(self, user_id: str, code: str) -> CodeModel:
        """
        Retrieves a verification code record associated with the given email, code, and minimum creation date.

        Args:
            email (str): Email associated with the verification code.
            code (str): Verification code.
            min_created (datetime): Minimum creation date for the verification code.

        Returns:
            CodeModel: Verification code record associated with the given parameters, or None if not found.
        """
        query = (
            select(CodeModel)
            .select_from(CodeModel)
            .where(
                CodeModel.code == code,
                CodeModel.user_id == user_id,
                # CodeModel.used_at is None
            )
        )
        result = self.session.execute(query).first()
        if result is None:
            return None
        code_model: CodeModel = result[0]
        return code_model
