from fastapi import APIRouter
from entities.dto.surnames_dto import CreateSurnameDto, ResponseSurnameDto, UpdateSurnameDto

from src.service.surnames_service import SurnamesService

surnames_router = APIRouter(
    prefix='/surnames',
    tags=['surnames']
)

surnames_service: SurnamesService = SurnamesService()


@surnames_router.get('/', response_model=list[ResponseSurnameDto])
def get():
    return surnames_service.get()


@surnames_router.get('/{id}', response_model=ResponseSurnameDto)
def get_by_id(id: int):
    return surnames_service.get_by_id(id)


@surnames_router.get('/', response_model=ResponseSurnameDto)
def get_by_surname(surname: str):
    return surnames_service.get_by_surname(surname)


@surnames_router.post('/', response_model=ResponseSurnameDto)
def create(dto: CreateSurnameDto):
    return surnames_service.create(dto)


@surnames_router.patch('/{id}', response_model=ResponseSurnameDto)
def update(id: int, dto: UpdateSurnameDto):
    return surnames_service.update(id, dto)


@surnames_router.delete('/{id}', )
def delete(id: int):
    return surnames_service.delete(id)
