from pydantic import BaseModel
from src.utils.AllOptional import AllOptional


class CreateSurnameDto(BaseModel):
    surname_ip: str
    surname_rp: str | None
    surname_dp: str | None
    surname_vp: str | None
    surname_tp: str | None
    surname_pp: str | None


class UpdateSurnameDto(CreateSurnameDto, metaclass=AllOptional):
    pass


class ResponseSurnameDto(CreateSurnameDto):
    pass
