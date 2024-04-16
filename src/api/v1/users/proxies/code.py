from datetime import datetime

from sqlalchemy import desc, select

from core.utils.repository_base import RepositoryBase
from models import (
    CodeModel,
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
                #CodeModel.used_at is None
            )
        )
        result = self.session.execute(query).first()
        if result is None:
            return None
        code_model: CodeModel = result[0]
        return code_model
