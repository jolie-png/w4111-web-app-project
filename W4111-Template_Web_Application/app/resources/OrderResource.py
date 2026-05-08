from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from .AbstractBaseResource import AbstractBaseResource
from ..services.MySQLDataService import MySQLDataService


class Order(BaseModel):
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str
    comments: Optional[str] = None
    customerNumber: int


class OrderCollection(BaseModel):
    items: list[Order] = Field(default_factory=list)


class OrderResource(AbstractBaseResource):
    def __init__(self, config: dict | None = None) -> None:
        if config is None:
            config = {}
        super().__init__(config)
        service_config = {
            "host": config.get("host"),
            "port": config.get("port"),
            "user": config.get("user"),
            "password": config.get("password"),
            "database": config.get("database"),
            "table_name": "orders",
            "primary_key_field": "orderNumber",
        }
        self._service = MySQLDataService(service_config)

    def get(self, template: dict) -> OrderCollection:
        rows = self._service.retrieveByTemplate(template)
        orders = []
        for row in rows:
            orders.append(Order.model_validate(row))
        return OrderCollection(items=orders)

    def get_by_id(self, id: str) -> Order:
        row = self._service.retrieveByPrimaryKey(str(id))
        if not row:
            raise ValueError("No order with orderNumber " + str(id))
        return Order.model_validate(row)

    def post(self, new_data: Order) -> str:
        data = new_data.model_dump(exclude_unset=True, mode="json")
        if "orderNumber" not in data:
            raise ValueError("orderNumber is required")
        return self._service.create(data)

    def put(self, character_id: str, new_data: Order) -> int:
        data = new_data.model_dump(exclude_unset=True, mode="json")
        return self._service.updateByPrimaryKey(str(character_id), data)

    def delete(self, id: str) -> int:
        return self._service.deleteByPrimaryKey(str(id))