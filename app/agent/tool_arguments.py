from pydantic import BaseModel, ConfigDict, Field


class SearchProductArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str

class GetOrderArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: int = Field(..., gt=0)

class CancelOrderArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: int = Field(..., gt=0)

class RefundOrderArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: int = Field(..., gt=0)
