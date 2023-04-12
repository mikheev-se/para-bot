from src.db.connection import get_session
from src.entities.dto.subjects_dto import CreateSubjectDto, UpdateSubjectDto
from src.entities.subject import Subject


class SubjectsRepository:
    def __init__(self, connection=next(get_session())) -> None:
        self.connection = connection

    def get(self) -> list[Subject]:
        subjects = (
            self.connection
            .query(Subject)
            .order_by('id')
            .all()
        )

        return subjects

    def get_by_id(self, id: int) -> Subject:
        subject = (
            self.connection
            .query(Subject)
            .filter(Subject.id == id)
            .first()
        )

        return subject

    def get_by_subject(self, subject: str) -> Subject:
        subject = (
            self.connection
            .query(Subject)
            .filter(Subject.subject == subject)
            .first()
        )

        return subject

    def get_by_subject_any_variant(self, subject: str) -> list[Subject]:
        subjects = (
            self.connection
            .query(Subject)
            .filter(
                (Subject.subject == subject) |
                (Subject.lemma == subject) |
                (Subject.acronym == subject)
            )
            .all()
        )

        return subjects

    def create(self, dto: CreateSubjectDto) -> Subject:
        subject = Subject(**dto.dict())
        self.connection.add(subject)
        self.connection.commit()

        return subject

    def update(self, id: int, dto: UpdateSubjectDto) -> Subject:
        subject = self.get_by_id(id)
        if not subject:
            return
        for field, value in dto:
            if value:
                setattr(subject, field, value)
        self.connection.commit()

        return subject

    def delete(self, id: int):
        subject = self.get_by_id(id)
        if not subject:
            return
        self.connection.delete(subject)
        self.connection.commit()
