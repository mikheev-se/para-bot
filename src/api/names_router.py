from fastapi import APIRouter
from entities.dto.names_dto import CreateNameDto, ResponseNameDto, UpdateNameDto

from src.service.names_service import NamesService

names_router = APIRouter(
    prefix='/names',
    tags=['names']
)

names_service: NamesService = NamesService()


@names_router.get('/', response_model=list[ResponseNameDto])
def get():
    return names_service.get()


@names_router.get('/{id}', response_model=ResponseNameDto)
def get_by_id(id: int):
    return names_service.get_by_id(id)


@names_router.get('/', response_model=ResponseNameDto)
def get_by_name(name: str):
    return names_service.get_by_name(name)


@names_router.post('/', response_model=ResponseNameDto)
def create(dto: CreateNameDto):
    return names_service.create(dto)


@names_router.patch('/{id}', response_model=ResponseNameDto)
def update(id: int, dto: UpdateNameDto):
    return names_service.update(id, dto)


@names_router.delete('/{id}')
def delete(id: int):
    return names_service.delete(id)
