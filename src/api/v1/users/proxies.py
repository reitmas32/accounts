from sqlalchemy import asc, func,desc
from models import CodeModel,UserModel
from core.utils.repository_base import RepositoryBase
from sqlalchemy import select,or_
from datetime import datetime
from sqlalchemy.orm import Session

class RepositoryUser(RepositoryBase):
    model = UserModel

    def exists_email_or_user_name(self, email: str, user_name: str) -> UserModel:
        query = select(self.model).where(
            or_(
                self.model.email == email,
                self.model.user_name == user_name
            )
        )
        result = self.session.execute(query).first()
        return result is not None


    def get_user(self, email: str) -> UserModel:
        query = select(self.model).where(
            self.model.email == email,
            self.model.validate == True
        )
        result = self.session.execute(query).first()
        return result[0] if result else None


    def get_last_user_with_specifi_email(self, email: str) -> UserModel:
        query = select(self.model).where(self.model.email == email).order_by(desc(self.model.created))
        result = self.session.execute(query).first()
        return result[0] if result else None


class RepositoryCode(RepositoryBase):
    model = CodeModel


    def get_code(self,email:str,code:str,min_created:datetime) -> CodeModel:

        query = select(CodeModel).select_from(CodeModel).where(
            CodeModel.email == email,
            CodeModel.code == code,
            CodeModel.used_at == None,
            CodeModel.created >= min_created
        ).order_by(desc(self.model.created))
        result = self.session.execute(query).one_or_none()
        return result[0] if result else None