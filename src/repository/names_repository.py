from src.db.connection import get_session
from src.entities.dto.names_dto import CreateNameDto, UpdateNameDto
from src.entities.name import Name


class NamesRepository:
    def __init__(self, connection=next(get_session())) -> None:
        self.connection = connection

    def get(self) -> list[Name]:
        names = (
            self.connection
            .query(Name)
            .order_by('name_ip')
            .all()
        )

        return names

    def get_by_id(self, id: int) -> Name:
        name = (
            self.connection
            .query(Name)
            .filter(Name.id == id)
            .first()
        )

        return name

    def get_by_name(self, name: str) -> Name:
        name = (
            self.connection
            .query(Name)
            .filter(Name.name_ip == name)
            .first()
        )

        return name

    def get_by_name_any_case(self, name: str) -> list[Name]:
        names = (
            self.connection
            .query(Name)
            .filter(
                (Name.name_ip == name) |
                (Name.name_rp == name) |
                (Name.name_dp == name) |
                (Name.name_vp == name) |
                (Name.name_tp == name) |
                (Name.name_pp == name)
            )
            .order_by('name_ip')
            .all()
        )

        return names

    def create(self, dto: CreateNameDto) -> Name:
        name = Name(**dto.dict())
        self.connection.add(name)
        self.connection.commit()

        return name

    def update(self, id: int, dto: UpdateNameDto) -> Name:
        name = self.get_by_id(id)
        if not name:
            return
        for field, value in dto:
            if value:
                setattr(name, field, value)
        self.connection.commit()

        return name

    def delete(self, id: int):
        name = self.get_by_id(id)
        if not name:
            return
        self.connection.delete(name)
        self.connection.commit()
