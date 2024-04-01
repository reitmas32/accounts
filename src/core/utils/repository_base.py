import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pytz import timezone
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.settings import log, settings
from core.utils.responses import get_current_date_time_to_app_standard


class RepositoryBase(ABC):
    """
    Abstract base class for database repositories.

    This class provides basic database operations and is intended to be
    inherited by specific repositories to manage particular models.
    Each subclass is expected to define the `model` property.

    Attributes
    ----------
    session : Session
        The active database session for executing queries.
    logger : Logger
        The logger to use for writing log messages.

    Examples
    --------
    >>> class UserRepository(RepositoryBase):
    ...     model = UserModel
    ...     # Implement any user-specific database methods here
    """

    @property
    @abstractmethod
    def model(self) -> type:
        """
        Abstract model property to be overridden by subclasses.

        This property should return the database model associated
        with a particular repository.

        Returns
        -------
        Type
            The class of the associated database model.
        """

    def __init__(self, session: Session):
        """
        Initialize the RepositoryBase with a database session.

        Parameters
        ----------
        session : Session
            The active database session for executing queries.
        """
        self.session = session
        self.logger = log

    def update_field_by_id(
        self, id: uuid.UUID, field_name: str, new_value: Any
    ) -> bool:
        """
        Update a specific field of a record in the database by its unique identifier.

        Parameters
        ----------
        id : uuid.UUID
            The unique identifier of the record.
        field_name : str
            The name of the field to be updated.
        new_value : Any
            The new value to set for the field.

        Returns
        -------
        bool
            True if the update was successful, otherwise it raises an exception.

        Examples
        --------
        >>> repo = UserRepository(session)
        >>> success = repo.update_field_by_id(some_uuid, "username", "new_username")
        """
        result = False
        try:
            # Construct a dynamic update query
            update_query = (
                self.session.query(self.model)
                .filter(self.model.id == id)
                .update({field_name: new_value})
            )

            # Commit the changes
            self.session.commit()

            # Return True if at least one row was affected
            result = update_query > 0

        except Exception as e:
            # Roll back the changes in case of errors
            self.session.rollback()
            # Raise the exception to inform the caller about the error
            raise e  # noqa: TRY201
        return result

    def get_by_id(self, id: uuid.UUID) -> type | None:
        """
        Retrieve a record from the database by its unique identifier.

        Parameters
        ----------
        id : uuid.UUID
            The unique identifier of the record.

        Returns
        -------
        Union[Type, None]
            An instance of the associated model if found, otherwise None.

        Examples
        --------
        >>> repo = UserRepository(session)
        >>> user = repo.get_by_id(some_uuid)
        """
        query = self.session.query(self.model).filter(self.model.id == id)
        return query.first()

    def get_by_attributes(
        self,
        return_query: bool = False,  # noqa: FBT001
        **filters: dict,
    ):
        """
        Retrieve records from the database based on multiple attribute-value pairs.

        Parameters
        ----------
        filters : dict
            A dictionary of attribute-value pairs.
        return_query : bool
            If True, return the query object instead of executing it.

        Returns
        -------
        List[Type] or "Query"
            A list of instances of the associated model or a Query object based on the return_query parameter.

        Examples
        --------
        >>> users = repo.get_by_attributes({"email": "example@example.com", "name": "John Doe"})
        >>> query = repo.get_by_attributes({"email": "example@example.com"}, return_query=True)
        """

        conditions = []
        for attribute, value in filters.items():
            if not hasattr(self.model, attribute):
                raise ValueError(
                    f"Attribute {attribute} not found in model {self.model.__name__}"
                )

            # Check if the value is a list, and use 'in_' if it is
            if isinstance(value, list):
                conditions.append(getattr(self.model, attribute).in_(value))
            else:
                conditions.append(getattr(self.model, attribute) == value)

        query = self.session.query(self.model).filter(and_(*conditions))

        if return_query:
            return query

        return query.all()

    def add(self, **kwargs) -> type | None:
        """
        Add a new record to the database.

        Parameters
        ----------
        **kwargs :
            Arbitrary keyword arguments which should match the columns of the model.

        Returns
        -------
        Union[Type, None]
            The newly created model instance if successful, otherwise None.

        Examples
        --------
        >>> repo = UserRepository(session)
        >>> new_user = repo.add(name="John", email="john@example.com")
        """
        new_record = None
        try:
            current_time = datetime.now(timezone(settings.TIME_ZONE))
            new_record = self.model(
                **kwargs, created=current_time, updated=current_time, is_removed=False
            )
            self.session.add(new_record)

            # Persist the record to the database
            self.session.flush()

            # Refresh the object to retrieve values generated by the database
            self.session.refresh(new_record)

            # Commit the record to the database
            self.session.commit()
        except SQLAlchemyError as e:
            # In case of an error, roll back the changes
            self.session.rollback()
            message_error = f"Failed to add a new record: {e}"
            raise SQLAlchemyError(message_error)  # noqa: B904
        return new_record

    def delete_by_id(self, id: uuid.UUID) -> bool:
        """
        Delete a record from the database by its unique identifier.

        Parameters
        ----------
        id : uuid.UUID
            The unique identifier of the record.

        Returns
        -------
        bool
            True if the deletion was successful, otherwise it raises an exception.

        Examples
        --------
        >>> repo = UserRepository(session)
        >>> success = repo.delete_by_id(some_uuid)
        """

        result = False
        try:
            # Construct a delete query
            delete_query = (
                self.session.query(self.model).filter(self.model.id == id).delete()
            )

            # Commit the changes
            self.session.commit()

            # Return True if at least one row was affected
            result = delete_query > 0

        except Exception as e:
            # Roll back the changes in case of errors
            self.session.rollback()
            # Raise the exception to inform the caller about the error
            log.error(e)
            raise e  # noqa: TRY201
        return result

    def _get_common_fields(self) -> dict:
        """
        Get the common fields used for various models.

        Returns
        -------
        dict
            A dictionary containing common field values.
        """

        current_time = get_current_date_time_to_app_standard()
        return {"created": current_time, "updated": current_time, "is_removed": False}
