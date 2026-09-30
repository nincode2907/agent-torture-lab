from pydantic import BaseModel, ConfigDict, Field


class SearchProductArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(
        ...,
        description="Product name or partial product name.",
    )

class GetOrderArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: int = Field(
        ...,
        gt=0,
        description="Order ID",
    )

class CancelOrderArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: int = Field(
        ...,
        gt=0,
        description="Order ID to cancel",
    )

class RefundOrderArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: int = Field(
        ...,
        gt=0,
        description="Order ID to refund",
    )
