from src.entities.dto.names_dto import CreateNameDto, UpdateNameDto
from src.entities.name import Name
from src.repository.names_repository import NamesRepository


class NamesService:
    def __init__(self, repository: NamesRepository = NamesRepository()) -> None:
        self.repository = repository

    def get(self) -> list[Name]:
        return self.repository.get()

    def get_by_id(self, id: int) -> Name:
        return self.repository.get_by_id(id)

    def get_by_name(self, name: str) -> Name:
        return self.repository.get_by_name(name)

    def get_by_name_any_case(self, name: str) -> list[Name]:
        return self.repository.get_by_name_any_case(name)

    def create(self, dto: CreateNameDto) -> Name:
        dto.name_ip = dto.name_ip.title()
        name = self.repository.create(dto)
        cases = self.inflect(name)
        update_cases_dto = cases
        update_cases_dto.update((field, value)
                                for field, value in dto if value is not None)
        update_cases_dto = UpdateNameDto(**update_cases_dto)
        return self.update(name.id, update_cases_dto)

    def update(self, id: int, dto: UpdateNameDto) -> Name:
        self.repository.update(id, dto)
        name = self.get_by_id(id)
        name.name_ip = name.name_ip.title()
        cases = self.inflect(name)
        update_cases_dto = cases
        update_cases_dto.update((field, value)
                                for field, value in dto if value is not None)
        update_cases_dto = UpdateNameDto(**update_cases_dto)
        return self.repository.update(id, update_cases_dto)

    def delete(self, id: int):
        self.repository.delete(id)

    @staticmethod
    def inflect(name_from_db: Name) -> dict[str, str]:
        name = name_from_db.name_ip
        sex = name_from_db.sex
        result = {
            'name_ip': name,
            'name_rp': name,
            'name_dp': name,
            'name_vp': name,
            'name_tp': name,
            'name_pp': name,
        }
        consonant = 'БВГДЖЗЙКЛМНПРСТФХЦЧШЩ'.lower()
        vowel = 'АИОУЫЭЕЁЮЯ'.lower()

        if name == 'Павел':
            name = 'Павл'
        elif name == 'Лев':
            name = 'Льв'

        if len(name) > 1 and ((sex == 'Ж' and name[-1] in consonant) or
                              (name[-1] != 'а' and name[-1]
                               != 'я' and name[-1] in vowel)):
            return result

        if name.endswith('й'):
            result['name_rp'] = name[:-1] + 'я'
            result['name_dp'] = name[:-1] + 'ю'
            result['name_vp'] = name[:-1] + 'я'
            result['name_tp'] = name[:-1] + 'ем'
            if name.endswith('ий'):
                result['name_pp'] = name[:-1] + 'и'
            else:
                result['name_pp'] = name[:-1] + 'е'
        elif name.endswith('иа') or name.endswith('я'):
            result['name_rp'] = name[:-1] + 'и'
            if name.endswith('ия'):
                result['name_dp'] = name[:-1] + 'и'
                result['name_pp'] = name[:-1] + 'и'
            else:
                result['name_dp'] = name[:-1] + 'е'
                result['name_pp'] = name[:-1] + 'е'
            result['name_vp'] = name[:-1] + 'ю'
            result['name_tp'] = name[:-1] + 'ей'
        elif name.endswith('а'):
            if name.endswith('жа') or name.endswith('ша'):
                result['name_rp'] = name[:-1] + 'и'
                result['name_tp'] = name[:-1] + 'ей'
            elif (name.endswith('га') or name.endswith('ка') or
                  name.endswith('ха') or name.endswith('ча')):
                result['name_rp'] = name[:-1] + 'и'
                result['name_tp'] = name[:-1] + 'ой'
            else:
                result['name_rp'] = name[:-1] + 'ы'
                result['name_tp'] = name[:-1] + 'ой'
            result['name_dp'] = name[:-1] + 'е'
            result['name_vp'] = name[:-1] + 'у'
            result['name_pp'] = name[:-1] + 'е'
        elif name.endswith('ь'):
            if not name.endswith('чь') and sex == 'М':
                result['name_rp'] = name[:-1] + 'я'
                result['name_dp'] = name[:-1] + 'ю'
                result['name_vp'] = name[:-1] + 'я'
                result['name_tp'] = name[:-1] + 'ем'
                result['name_pp'] = name[:-1] + 'е'
            else:
                result['name_rp'] = name[:-1] + 'и'
                result['name_dp'] = name[:-1] + 'и'
                result['name_vp'] = name
                result['name_tp'] = name + 'ю'
                result['name_pp'] = name[:-1] + 'и'
        elif len(name) > 1:
            result['name_rp'] = name + 'а'
            result['name_dp'] = name + 'у'
            result['name_vp'] = name + 'а'
            result['name_tp'] = name + 'ом'
            result['name_pp'] = name + 'е'

        return result
