import datetime
from typing import Literal
from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class SuccessResponse(BaseModel):
    status: Literal['success']

class CreateAdvertRequest(BaseModel):
    title: str
    description: str
    prise: int
    autor: str


class CreateAdvertResponse(IdResponse):
    pass


class UpdateAdvertRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    prise: int | None = None
    autor: str | None = None


class UpdateAdvertResponse(SuccessResponse):
    pass


class GetAdvertResponse(BaseModel):
    id: int
    title: str| None
    description: str| None
    prise: int| None
    autor: str | None
    created_at: datetime.datetime


class SearchAdvertResponse(BaseModel):
    results: list[GetAdvertResponse]


class DeleteAdvertResponse(SuccessResponse):
    pass


# class LoginRequest(BaseModel):
#     name: str
#     password: str
#
#
# class LoginResponse(BaseModel):
#     token: str

