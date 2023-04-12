from src.db.connection import get_session
from src.entities.dto.surnames_dto import CreateSurnameDto, UpdateSurnameDto
from src.entities.surname import Surname


class SurnamesRepository:
    def __init__(self, connection=next(get_session())) -> None:
        self.connection = connection

    def get(self) -> list[Surname]:
        surnames = (
            self.connection
            .query(Surname)
            .order_by('surname_ip')
            .all()
        )

        return surnames

    def get_by_id(self, id: int) -> Surname:
        surname = (
            self.connection
            .query(Surname)
            .filter(Surname.id == id)
            .first()
        )

        return surname

    def get_by_surname(self, surname: str) -> Surname:
        surname = (
            self.connection
            .query(Surname)
            .filter(Surname.surname_ip == surname)
            .first()
        )

        return surname

    def get_by_surname_any_case(self, surname: str) -> list[Surname]:
        surnames = (
            self.connection
            .query(Surname)
            .filter(
                (Surname.surname_ip == surname) |
                (Surname.surname_rp == surname) |
                (Surname.surname_dp == surname) |
                (Surname.surname_vp == surname) |
                (Surname.surname_tp == surname) |
                (Surname.surname_pp == surname)
            )
            .all()
        )

        return surnames

    def create(self, dto: CreateSurnameDto) -> Surname:
        surname = Surname(**dto.dict())
        self.connection.add(surname)
        self.connection.commit()

        return surname

    def update(self, id: int, dto: UpdateSurnameDto) -> Surname:
        surname = self.get_by_id(id)
        if not surname:
            return
        for field, value in dto:
            if value:
                setattr(surname, field, value)
        self.connection.commit()

        return surname

    def delete(self, id: int):
        surname = self.get_by_id(id)
        if not surname:
            return
        self.connection.delete(surname)
        self.connection.commit()
