from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .AbstractBaseResource import AbstractBaseResource
from ..services.MySQLDataService import MySQLDataService


class Customer(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None


class CustomerCollection(BaseModel):
    items: list[Customer] = Field(default_factory=list)


class CustomerResource(AbstractBaseResource):
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
            "table_name": "customers",
            "primary_key_field": "customerNumber",
        }
        self._service = MySQLDataService(service_config)

    def get(self, template: dict) -> CustomerCollection:
        rows = self._service.retrieveByTemplate(template)
        customers = []
        for row in rows:
            customers.append(Customer.model_validate(row))
        return CustomerCollection(items=customers)

    def get_by_id(self, id: str) -> Customer:
        row = self._service.retrieveByPrimaryKey(str(id))
        if not row:
            raise ValueError("No customer with customerNumber " + str(id))
        return Customer.model_validate(row)

    def post(self, new_data: Customer) -> str:
        data = new_data.model_dump(exclude_unset=True)
        if "customerNumber" not in data:
            raise ValueError("customerNumber is required")
        return self._service.create(data)

    def put(self, character_id: str, new_data: Customer) -> int:
        data = new_data.model_dump(exclude_unset=True)
        data["customerNumber"] = int(character_id)
        return self._service.updateByPrimaryKey(str(character_id), data)

    def delete(self, id: str) -> int:
        return self._service.deleteByPrimaryKey(str(id))