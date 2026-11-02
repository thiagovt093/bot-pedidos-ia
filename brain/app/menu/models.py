from __future__ import annotations

from pydantic import BaseModel, Field


class ComplementOption(BaseModel):
    name: str
    price: float


class Complement(BaseModel):
    category: str
    required: bool
    options: list[ComplementOption]


class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    complements: list[Complement] = Field(default_factory=list)
