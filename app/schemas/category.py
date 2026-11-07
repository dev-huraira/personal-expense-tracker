from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CategoryType = Literal["income", "expense"]


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    type: CategoryType


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    type: CategoryType | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: CategoryType

    model_config = ConfigDict(from_attributes=True)