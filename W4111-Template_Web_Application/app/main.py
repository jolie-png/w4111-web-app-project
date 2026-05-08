from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.resources.CustomerResource import (
    CustomerResource,
    Customer,
    CustomerCollection,
)
from app.resources.OrderResource import (
    OrderResource,
    Order,
    OrderCollection,
)
from app.resources.OrderDetailsResource import (
    OrderDetailsResource,
    OrderDetail,
    OrderDetailsCollection,
)

customer_resource = CustomerResource()
order_resource = OrderResource()
order_details_resource = OrderDetailsResource()




if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from app.resources.HarryPotterResource import (
        HarryPotterCharacter,
        HarryPotterCollection,
        HarryPotterResource,
    )
else:
    from .resources.HarryPotterResource import (
        HarryPotterCharacter,
        HarryPotterCollection,
        HarryPotterResource,
    )


def _get_app_name() -> str:
    return os.getenv("APP_NAME", "Starter FastAPI App")


app = FastAPI(title=_get_app_name(), version="0.1.0")
harry_potter_resource = HarryPotterResource()


class EchoRequest(BaseModel):
    message: str


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {"message": "Hello from FastAPI"}


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/echo", tags=["echo"])
def echo(payload: EchoRequest) -> EchoRequest:
    return payload


@app.get("/harry-potter", tags=["harry-potter"])
def get_harry_potter_characters(
    first_name: str | None = None,
    last_name: str | None = None,
    house_name: str | None = None,
) -> HarryPotterCollection:
    template: dict = {}
    if first_name is not None:
        template["first_name"] = first_name
    if last_name is not None:
        template["last_name"] = last_name
    if house_name is not None:
        template["house_name"] = house_name
    return harry_potter_resource.get(template)


@app.get("/harry-potter/{character_id}", tags=["harry-potter"])
def get_harry_potter_character_by_id(character_id: str) -> HarryPotterCharacter:
    try:
        return harry_potter_resource.get_by_id(character_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/harry-potter", tags=["harry-potter"])
def create_harry_potter_character(new_data: HarryPotterCharacter) -> str:
    new_id = harry_potter_resource.post(new_data)
    return str(new_id)


@app.put("/harry-potter/{character_id}", tags=["harry-potter"])
def update_harry_potter_character(
    character_id: str, new_data: HarryPotterCharacter
) -> dict[str, int]:
    try:
        updated = harry_potter_resource.put(character_id, new_data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"updated": updated}


@app.delete("/harry-potter/{character_id}", tags=["harry-potter"])
def delete_harry_potter_character(character_id: str) -> dict[str, int]:
    deleted = harry_potter_resource.delete(character_id)
    return {"deleted": deleted}




@app.get("/customers", tags=["customers"])
def get_customers(
    city: str | None = None,
    country: str | None = None,
) -> CustomerCollection:
    template: dict = {}
    if city is not None:
        template["city"] = city
    if country is not None:
        template["country"] = country
    return customer_resource.get(template)


@app.post("/customers", tags=["customers"], status_code=201)
def create_customer(new_customer: Customer) -> str:
    try:
        new_id = customer_resource.post(new_customer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return str(new_id)



@app.get("/customers/{customerNumber}", tags=["customers"])
def get_customer_by_id(customerNumber: int) -> Customer:
    try:
        return customer_resource.get_by_id(str(customerNumber))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.put("/customers/{customerNumber}", tags=["customers"])
def update_customer(
    customerNumber: int, new_data: Customer
) -> dict[str, int]:
    try:
        updated = customer_resource.put(str(customerNumber), new_data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"updated": updated}


@app.delete("/customers/{customerNumber}", tags=["customers"])
def delete_customer(customerNumber: int) -> dict[str, int]:
    deleted = customer_resource.delete(str(customerNumber))
    return {"deleted": deleted}

@app.get("/orders", tags=["orders"])
def get_orders(
    status: str | None = None,
    customerNumber: int | None = None,
) -> OrderCollection:
    template: dict = {}
    if status is not None:
        template["status"] = status
    if customerNumber is not None:
        template["customerNumber"] = customerNumber
    return order_resource.get(template)


@app.post("/orders", tags=["orders"], status_code=201)
def create_order(new_order: Order) -> str:
    try:
        new_id = order_resource.post(new_order)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return str(new_id)


@app.get("/orders/{orderNumber}", tags=["orders"])
def get_order_by_id(orderNumber: int) -> Order:
    try:
        return order_resource.get_by_id(str(orderNumber))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.put("/orders/{orderNumber}", tags=["orders"])
def update_order(orderNumber: int, new_data: Order) -> dict[str, int]:
    try:
        updated = order_resource.put(str(orderNumber), new_data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"updated": updated}


@app.delete("/orders/{orderNumber}", tags=["orders"])
def delete_order(orderNumber: int) -> dict[str, int]:
    deleted = order_resource.delete(str(orderNumber))
    return {"deleted": deleted}


@app.get("/orderdetails", tags=["orderdetails"])
def get_orderdetails(
    orderNumber: int | None = None,
    productCode: str | None = None,
) -> OrderDetailsCollection:
    template: dict = {}
    if orderNumber is not None:
        template["orderNumber"] = orderNumber
    if productCode is not None:
        template["productCode"] = productCode
    return order_details_resource.get(template)


@app.post("/orderdetails", tags=["orderdetails"], status_code=201)
def create_orderdetail(new_detail: OrderDetail) -> str:
    try:
        new_id = order_details_resource.post(new_detail)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return str(new_id)


@app.get("/orders/{orderNumber}/orderdetails/{productCode}", tags=["orderdetails"])
def get_order_detail(orderNumber: int, productCode: str) -> OrderDetail:
    composite_id = f"{orderNumber}|{productCode}"
    try:
        return order_details_resource.get_by_id(composite_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.put("/orders/{orderNumber}/orderdetails/{productCode}", tags=["orderdetails"])
def update_order_detail(
    orderNumber: int, productCode: str, new_data: OrderDetail
) -> dict[str, int]:
    composite_id = f"{orderNumber}|{productCode}"
    try:
        updated = order_details_resource.put(composite_id, new_data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"updated": updated}


@app.delete("/orders/{orderNumber}/orderdetails/{productCode}", tags=["orderdetails"])
def delete_order_detail(orderNumber: int, productCode: str) -> dict[str, int]:
    composite_id = f"{orderNumber}|{productCode}"
    deleted = order_details_resource.delete(composite_id)
    return {"deleted": deleted}
    
if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(app, host=host, port=port)

