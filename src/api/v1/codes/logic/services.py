from fastapi import status

from api.v1.codes.crud.proxies import CodeProxy
from api.v1.codes.crud.schemas import ListCodeSchema
from api.v1.codes.logic.schemas import ResentCodeSchema
from core.utils.generic_views import BaseService
from core.utils.responses import create_simple_envelope_response


class CreateCodesService(BaseService):
    model = CodeProxy
    schema = ListCodeSchema

    def _validate_request(self, payload: ResentCodeSchema):
        pass

    def create(self, payload: ResentCodeSchema):
        self.request_errors = {"validations_errors": {}, "validations_success": True}
        self._validate_request(payload=payload)

        instance = self.model(**payload.model_dump())
        self.session.add(instance)
        self.session.commit()

        return create_simple_envelope_response(
            data=instance.dict(),
            message="Code Created successfully",
            status_code=status.HTTP_201_CREATED,
            successful=True,
        )
