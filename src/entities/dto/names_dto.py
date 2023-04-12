from typing import Literal
from pydantic import BaseModel
from src.utils.AllOptional import AllOptional


class CreateNameDto(BaseModel):
    name_ip: str
    name_rp: str | None
    name_dp: str | None
    name_vp: str | None
    name_tp: str | None
    name_pp: str | None
    sex: Literal['М', 'Ж']


class UpdateNameDto(CreateNameDto, metaclass=AllOptional):
    pass


class ResponseNameDto(CreateNameDto):
    pass
