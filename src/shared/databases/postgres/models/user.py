import uuid

from sqlalchemy import JSON, Column, Date, String, event

from shared.databases.postgres.models.base_model import BaseModelClass


class UserModel(BaseModelClass):
    """
    Model for storing user information. This class captures essential user details such as
    name, birthday, and additional data in JSON format. It also includes functionality to
    generate a default username if not provided.

    Inherits common fields and behavior from BaseModelClass.

    Attributes:
    -----------
    - `user_name`: String representing the user's unique username.
    - `name`: String storing the full name of the user.
    - `birthday`: Date field representing the user's birthday.
    - `extra_data`: JSON field that stores any additional information related to the user.

    Methods:
    --------
    - `generate_default_username`: Static method to generate a default username using a UUID if no username is provided.

    Events:
    -------
    - The `before_insert` event triggers the `generate_default_username` method before inserting a new record.
    """

    __tablename__ = "users"  # Specifies the table name in the database

    user_name = Column(String, nullable=True)
    """String representing the user's unique username. If not provided, a default username is generated."""

    name = Column(String, nullable=True)
    """String representing the user's full name."""

    birthday = Column(Date, nullable=True)
    """Date field storing the user's birthday."""

    extra_data = Column(JSON, nullable=True)
    """JSON field storing any additional data related to the user, such as preferences or settings."""

    @staticmethod
    def generate_default_username(target, connection, **kw):  # noqa: ARG004
        """
        Static method that generates a default username if none is provided.
        The username is generated using the format `User<UUID>`.

        Parameters:
        -----------
        - `target`: The target instance of the UserModel being inserted.
        - `connection`: The database connection object.
        - `kw`: Additional keyword arguments (unused).
        """
        if target.user_name is None:
            target.user_name = f"User{uuid.uuid4()}"
            """Generate a default username in the format 'User<UUID>' if `user_name` is None."""


# Asociar el evento `before_insert` para llamar a `generate_default_username`
@event.listens_for(UserModel, "before_insert")
def set_default_username(mapper, connection, target):
    UserModel.generate_default_username(target, connection)
