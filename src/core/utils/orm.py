# Standard Library
from typing import Generic, TypeVar

# Third Party Stuff
from sqlalchemy import desc, func, select

T = TypeVar("T")


class Manager(Generic[T]):
    query = None
    cls = None

    def __init__(self: type[T]) -> None:
        pass

    def __get__(self, instance, owner):
        self.cls: T = owner
        self.query: select = select(self.cls)
        if hasattr(self.cls, "is_removed"):
            self.query = self.query.where(self.cls.is_removed.is_(False))
        return self

    def scalars(self):
        return self.cls.session.execute(self.query).scalars()

    def get_default_column(self, column):
        if not column:
            column = self.cls.__table__.columns[0]
            if hasattr(self.cls, "id"):
                column = self.cls.id
        return column

    def create(self: type[T], **kwargs: dict) -> T:
        instance = self.cls(**kwargs)
        self.cls.session.add(instance)
        instance.save()
        return instance

    def get(self, *args, **kwargs) -> T:
        self = self.filter(*args, **kwargs)  # noqa: PLW0642
        return self.scalars().one_or_none()

    def all(self) -> list[T]:
        return self.scalars().all()

    def first(self, column=None) -> T:
        if column is not None:
            self.query = self.query.order_by(column)
        return self.scalars().first()

    def last(self, column=None) -> T:
        if column is None:
            column = desc(self.cls.created)
        self.query = self.query.order_by(column)
        return self.scalars().first()

    def filter(self, *args, **kwargs):
        self.query = self.query.where(*args).filter_by(**kwargs)
        return self

    def deleted(self):
        self.query: select = select(self.cls)
        if hasattr(self.cls, "is_removed"):
            self.query = self.query.where(self.cls.is_removed.is_(True))
        return self

    def count(self, column=None) -> int:
        column = self.get_default_column(column)
        query = self.query.with_only_columns(func.count(column))
        return self.cls.session.execute(query).scalar_one()

    def exclude(self, *args, **kwargs):  # noqa: ARG002
        self.query = self.query.where(func.not_(*args))
        return self

    def order_by(self, *args, **kwargs):  # noqa: ARG002
        self.query = self.query.order_by(*args)
        return self

    def values(self, *columns):
        self.query = self.query.with_only_columns(*columns)
        return self

    def limit(self, limit):
        self.query = self.query.limit(limit)
        return self

    def offset(self, offset):
        self.query = self.query.offset(offset)
        return self

    def delete(self, hard=False):
        results = self.scalars().all()
        for record in results:
            record.delete(hard)

    def get_or_create(self, defaults=None, **kwargs) -> tuple[T, bool]:
        instance = self.filter(**kwargs).first()
        if instance:
            return instance, False
        else:  # noqa: RET505
            kwargs.update(defaults or {})
            instance = self.create(**kwargs)
            return instance, True

    def update_or_create(self, defaults=None, **kwargs) -> tuple[T, bool]:
        if defaults is None:
            defaults = {}
        instance, created = self.get_or_create(**kwargs, defaults=defaults)
        if not created:
            for key, value in defaults.items():
                setattr(instance, key, value)
            instance.save()
        return instance, created


class QueryModel:
    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def delete(self, hard=False) -> None:
        if hasattr(self, "is_removed"):
            self.is_removed = True
        if hard:
            self.session.delete(self)
        self.save()

    def save(self) -> T:
        self.session.commit()
        return self
