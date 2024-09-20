from abc import ABC, abstractmethod

from fastapi import HTTPException

from core.settings import log
from shared.app.errors.saga import SAGAError


class TransactionFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Transaction failed. Reverting changes.")


class StepSAGA(ABC):
    @abstractmethod
    def __call__(self, payload=None, all_payloads: dict | None = None):
        pass

    @abstractmethod
    def rollback(self):
        pass


class SagaController:
    def __init__(self, steps: list[StepSAGA]):
        self.steps = steps
        self.payloads = {}

    def execute(self):
        last_payload = None
        # Ejecutar los pasos de la transacción
        # TODO: sedebe retornar un dict de los payloads de cada call
        for step in self.steps:
            try:
                last_payload = step(payload=last_payload, all_payloads=self.payloads)
                self.payloads[type(step)] = last_payload
            except Exception as e:  # noqa: PERF203, BLE001
                self.rollback()
                raise SAGAError(e)
        return self.payloads

    def rollback(self):
        # Deshacer los pasos de la transacción en orden inverso
        for step in reversed(self.steps):
            try:
                step.rollback()
            except Exception as e:  # noqa: PERF203, BLE001
                # Si no se puede deshacer un paso, registrar el error y continuar
                log.error(f"Failed to rollback step: {type(step).__name__}, Error: {e}")
