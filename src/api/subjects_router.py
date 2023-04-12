from fastapi import APIRouter
from entities.dto.subjects_dto import CreateSubjectDto, ResponseSubjectDto, UpdateSubjectDto

from src.service.subjects_service import SubjectsService

subjects_router = APIRouter(
    prefix='/subjects',
    tags=['subjects']
)

subjects_service: SubjectsService = SubjectsService()


@subjects_router.get('/', response_model=list[ResponseSubjectDto])
def get():
    return subjects_service.get()


@subjects_router.get('/{id}', response_model=ResponseSubjectDto)
def get_by_id(id: int):
    return subjects_service.get_by_id(id)


@subjects_router.get('/subject/', response_model=ResponseSubjectDto)
def get_by_subject(subject: str):
    return subjects_service.get_by_subject(subject)


@subjects_router.post('/', response_model=ResponseSubjectDto)
def create(dto: CreateSubjectDto):
    return subjects_service.create(dto)


@subjects_router.patch('/{id}', response_model=ResponseSubjectDto)
def update(id: int, dto: UpdateSubjectDto):
    return subjects_service.update(id, dto)


@subjects_router.delete('/{id}')
def delete(id: int):
    return subjects_service.delete(id)
