from src.entities.dto.subjects_dto import CreateSubjectDto, UpdateSubjectDto
from src.entities.subject import Subject
from src.repository.subjects_repository import SubjectsRepository
import spacy


class SubjectsService:
    def __init__(self, repository: SubjectsRepository = SubjectsRepository()) -> None:
        self.repository = repository

    def get(self) -> list[Subject]:
        return self.repository.get()

    def get_by_id(self, id: int) -> Subject:
        return self.repository.get_by_id(id)

    def get_by_subject(self, subject: str) -> Subject:
        return self.repository.get_by_subject(subject)

    def get_by_subject_any_variant(self, subject: str) -> list[Subject]:
        return self.repository.get_by_subject_any_variant(subject)

    def create(self, dto: CreateSubjectDto) -> Subject:
        dto.subject = dto.subject.title()
        subject = self.repository.create(dto)
        acronym_and_lemma = self.acronym_and_lemma(subject)
        update_dto = acronym_and_lemma
        update_dto.update((field, value)
                          for field, value in dto if value is not None)
        update_dto = UpdateSubjectDto(**update_dto)
        return self.update(subject.id, update_dto)

    def update(self, id: int, dto: UpdateSubjectDto) -> Subject:
        self.repository.update(id, dto)
        subject = self.get_by_id(id)
        subject.subject = subject.subject.title()
        acronym_and_lemma = self.acronym_and_lemma(subject)
        update_dto = acronym_and_lemma
        update_dto.update((field, value)
                          for field, value in dto if value is not None)
        update_dto = UpdateSubjectDto(**update_dto)
        return self.repository.update(id, update_dto)

    def delete(self, id: int):
        self.repository.delete(id)

    @staticmethod
    def acronym_and_lemma(subject: Subject):
        acronym = ''.join(x[0] for x in subject.subject.split(
            ' ')) if len(subject.subject.split(' ')) > 1 else None
        nlp = spacy.load('ru_core_news_md')
        doc = nlp(subject.subject)
        lemma = ' '.join(token.lemma_ for token in doc)

        return {'lemma': lemma, 'acronym': acronym}
