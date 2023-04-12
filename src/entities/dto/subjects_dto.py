from pydantic import BaseModel
from src.utils.AllOptional import AllOptional


class CreateSubjectDto(BaseModel):
    subject: str
    lemma: str | None
    acronym: str | None


class UpdateSubjectDto(CreateSubjectDto, metaclass=AllOptional):
    pass


class ResponseSubjectDto(CreateSubjectDto):
    pass
