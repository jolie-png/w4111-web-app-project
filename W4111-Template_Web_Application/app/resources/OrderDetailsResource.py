from __future__ import annotations

from pydantic import BaseModel, Field

from .AbstractBaseResource import AbstractBaseResource
from ..services.MySQLDataService import MySQLDataService


class OrderDetail(BaseModel):
    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: float
    orderLineNumber: int


class OrderDetailsCollection(BaseModel):
    items: list[OrderDetail] = Field(default_factory=list)


class OrderDetailsResource(AbstractBaseResource):
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
            "table_name": "orderdetails",
            "primary_key_field": "orderNumber",
        }
        self._service = MySQLDataService(service_config)

    def get(self, template: dict) -> OrderDetailsCollection:
        rows = self._service.retrieveByTemplate(template)
        details = []
        for row in rows:
            details.append(OrderDetail.model_validate(row))
        return OrderDetailsCollection(items=details)

    def get_by_id(self, id: str) -> OrderDetail:
        parts = id.split("|", 1)
        if len(parts) != 2:
            raise ValueError("Invalid id format; expected 'orderNumber|productCode'")
        order_num_str = parts[0]
        product_code = parts[1]
        template = {"orderNumber": int(order_num_str), "productCode": product_code}
        rows = self._service.retrieveByTemplate(template)
        if not rows:
            raise ValueError(
                "No orderdetail with orderNumber=" + repr(order_num_str) + ", productCode=" + repr(product_code)
            )
        return OrderDetail.model_validate(rows[0])

    def post(self, new_data: OrderDetail) -> str:
        data = new_data.model_dump(exclude_unset=True)
        if "orderNumber" not in data or "productCode" not in data:
            raise ValueError("orderNumber and productCode are required")
        self._service.create(data)
        return str(data["orderNumber"]) + "|" + data["productCode"]

    def put(self, id: str, new_data: OrderDetail) -> int:
        parts = id.split("|", 1)
        if len(parts) != 2:
            raise ValueError("Invalid id format; expected 'orderNumber|productCode'")
        order_num_str = parts[0]
        product_code = parts[1]
        data = new_data.model_dump(exclude_unset=True)
        data.pop("orderNumber", None)
        data.pop("productCode", None)
        if not data:
            return 0
        template = {"orderNumber": int(order_num_str), "productCode": product_code}
        return self._service.updateByTemplate(template, data)

    def delete(self, id: str) -> int:
        parts = id.split("|", 1)
        if len(parts) != 2:
            raise ValueError("Invalid id format; expected 'orderNumber|productCode'")
        order_num_str = parts[0]
        product_code = parts[1]
        template = {"orderNumber": int(order_num_str), "productCode": product_code}
        return self._service.deleteByTemplate(template)