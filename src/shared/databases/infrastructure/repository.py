import uuid
from abc import ABC, abstractmethod
from typing import Any

from shared.app.errors.unimplemented import UnimplementedError


class RepositoryInterface(ABC):
    """
    Abstract interface defining the basic methods of a repository.
    """

    @property
    @abstractmethod
    def model(self) -> type:
        """
        Returns the database model associated with the repository.
        """
        raise UnimplementedError(resource="RepositoryInterface.model")

    @abstractmethod
    def update_field_by_id(self, id: uuid.UUID, field_name: str, new_value: Any) -> bool:
        """
        Updates a specific field of a record in the model by its ID.

        :param id: UUID of the record to update.
        :param field_name: Name of the field to update.
        :param new_value: New value of the field.
        :return: True if the update was successful, False otherwise.
        """
        raise UnimplementedError(resource="RepositoryInterface.update_field_by_id")

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Any | None:
        """
        Retrieves a record from the model by its ID.

        :param id: UUID of the record to retrieve.
        :return: The instance of the model if found, None otherwise.
        """
        raise UnimplementedError(resource="RepositoryInterface.get_by_id")

    @abstractmethod
    def get_all(self) -> list[Any]:
        """
        Returns all records from the model.

        :return: List of model instances.
        """
        raise UnimplementedError(resource="RepositoryInterface.get_all")

    @abstractmethod
    def get_by_attributes(self, **filters: Any) -> Any:
        """
        Retrieves records filtered by specific attributes.

        :param filters: Dictionary of attributes to filter the records.
        :return: Filtered results or the query if `return_query` is True.
        """
        raise UnimplementedError(resource="RepositoryInterface.get_by_attributes")

    @abstractmethod
    def add(self, **kwargs: Any) -> Any | None:
        """
        Adds a new record to the model.

        :param kwargs: Arguments representing the fields of the model.
        :return: The newly added instance of the model, or None if there was an error.
        """
        raise UnimplementedError(resource="RepositoryInterface.add")

    @abstractmethod
    def delete_by_id(self, id: uuid.UUID) -> bool:
        """
        Deletes a record from the model by its ID.

        :param id: UUID of the record to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        raise UnimplementedError(resource="RepositoryInterface.delete_by_id")
