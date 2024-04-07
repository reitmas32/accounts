from core.settings import settings
from core.utils.exceptions import FilterException


class ManagerFilter:
    separator = "__"

    def __init__(self, model, filters: dict) -> None:
        self.model = model
        self.filters = filters
        self.single_filters, self.range_filters, self.ordering = self.separe_filters(filters)

    def separe_filters(self, filters: dict):
        single_filters = {}
        range_filters = {}
        ordering = [settings.DEFAULT_ORDER_FIELD]

        for key, value in filters.items():
            if self.separator in key:
                range_filters.update({key: value})
            elif key == "ordering":
                ordering = value.split(",") if "," in value else [value]
            else:
                single_filters.update({key: value})
        return single_filters, range_filters, ordering

    def clean_order_by_keys(self, ordering_keys: list) -> list:
        cleaned_data = []
        invalid_keys = []
        valid_keys = self.model.__table__.columns.keys()

        for key in ordering_keys:
            clean_key = key.replace("-", "", 1)
            if not clean_key:
                continue
            if clean_key in valid_keys:
                cleaned_data.append(key)
            else:
                invalid_keys.append(key)

        if invalid_keys:
            raise FilterException(invalid_keys=invalid_keys, valid_keys=valid_keys)
        return cleaned_data

    def get_unary_expressions(self):
        unary_expressions = []

        for key, value in self.range_filters.items():
            field_name, operator = key.split(self.separator)

            columna = getattr(self.model, field_name)

            if operator == "gt":
                unary_expressions.append(columna > value)
            elif operator == "lt":
                unary_expressions.append(columna < value)
            elif operator == "gte":
                unary_expressions.append(columna >= value)
            elif operator == "lte":
                unary_expressions.append(columna <= value)
            elif operator == "contains":
                unary_expressions.append(columna.like(value))
            elif operator == "icontains":
                unary_expressions.append(columna.ilike(value))

        return unary_expressions

    def get_ordering_expressions(self) -> list:
        ordering_cleaned = self.clean_order_by_keys(self.ordering)
        order_by = []

        for key in ordering_cleaned:
            clean_key = key.replace("-", "", 1)
            order_item = getattr(self.model, clean_key).asc()
            if key.startswith("-"):
                order_item = getattr(self.model, clean_key).desc()

            order_by.append(order_item)

        return order_by

    def manage_filters(self) -> tuple[list, dict, list]:
        unary_expressions = self.get_unary_expressions()
        order_by = self.get_ordering_expressions()

        return unary_expressions, self.single_filters, order_by
