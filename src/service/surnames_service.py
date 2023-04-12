from src.entities.dto.surnames_dto import CreateSurnameDto, UpdateSurnameDto
from src.entities.surname import Surname
from src.repository.surnames_repository import SurnamesRepository


class SurnamesService:
    def __init__(self, repository: SurnamesRepository = SurnamesRepository()) -> None:
        self.repository = repository

    def get(self) -> list[Surname]:
        return self.repository.get()

    def get_by_id(self, id: int) -> Surname:
        return self.repository.get_by_id(id)

    def get_by_surname(self, surname: str) -> Surname:
        return self.repository.get_by_surname(surname)

    def get_by_surname_any_case(self, surname: str) -> list[Surname]:
        return self.repository.get_by_surname_any_case(surname)

    def create(self, dto: CreateSurnameDto) -> Surname:
        dto.surname_ip = dto.surname_ip.title()
        surname = self.repository.create(dto)
        cases = self.inflect(surname)
        update_cases_dto = cases
        update_cases_dto.update((field, value)
                                for field, value in dto if value is not None)
        update_cases_dto = UpdateSurnameDto(**update_cases_dto)
        return self.update(surname.id, update_cases_dto)

    def update(self, id: int, dto: UpdateSurnameDto) -> Surname:
        self.repository.update(id, dto)
        surname = self.get_by_id(id)
        surname.surname_ip = surname.surname_ip.title()
        cases = self.inflect(surname)
        update_cases_dto = cases
        update_cases_dto.update((field, value)
                                for field, value in dto if value is not None)
        update_cases_dto = UpdateSurnameDto(**update_cases_dto)
        return self.repository.update(id, update_cases_dto)

    def delete(self, id: int):
        self.repository.delete(id)

    @staticmethod
    def inflect(surname_from_db: Surname) -> dict[str, str]:
        surname = surname_from_db.surname_ip
        result = {
            'surname_ip': surname,
            'surname_rp': surname,
            'surname_dp': surname,
            'surname_vp': surname,
            'surname_tp': surname,
            'surname_pp': surname,
        }
        consonant = 'БВГДЖЗЙКЛМНПРСТФХЦЧШЩ'.lower()
        vowel = 'АИОУЫЭЕЁЮЯ'.lower()

        if (surname.endswith('ых') or surname.endswith('их') or
                (len(surname) > 1 and (
                    surname[-1] in 'еиоуыэю' or (surname.endswith('а')
                                                 and surname[-2] in vowel)
                ))):
            return result

        if surname.endswith('ев') or surname.endswith('ов') or surname.endswith('ин'):
            result['surname_rp'] = surname + 'а'
            result['surname_dp'] = surname + 'у'
            result['surname_vp'] = surname + 'а'
            result['surname_tp'] = surname + 'ым'
            result['surname_pp'] = surname + 'е'

        elif surname.endswith('ева') or surname.endswith('ова') or surname.endswith('ина'):
            result['surname_rp'] = surname[:-1] + 'ой'
            result['surname_dp'] = surname[:-1] + 'ой'
            result['surname_vp'] = surname[:-1] + 'у'
            result['surname_tp'] = surname[:-1] + 'ой'
            result['surname_pp'] = surname[:-1] + 'ой'

        elif surname.endswith('ый') or surname.endswith('ий'):
            result['surname_rp'] = surname[:-2] + 'ого'
            result['surname_dp'] = surname[:-2] + 'ому'
            result['surname_vp'] = surname[:-2] + 'ого'
            result['surname_pp'] = surname[:-2] + 'ом'
            if surname.endswith('ый'):
                result['surname_tp'] = surname[:-2] + 'ым'
            elif surname.endswith('ий'):
                result['surname_tp'] = surname[:-2] + 'им'

        elif surname.endswith('ая'):
            if len(surname) > 3:
                if surname[-3] in 'чшщ':
                    result['surname_rp'] = surname[:-2] + 'ей'
                    result['surname_dp'] = surname[:-2] + 'ей'
                    result['surname_vp'] = surname[:-2] + 'ую'
                    result['surname_tp'] = surname[:-2] + 'ей'
                    result['surname_pp'] = surname[:-2] + 'ей'
                else:
                    result['surname_rp'] = surname[:-2] + 'ой'
                    result['surname_dp'] = surname[:-2] + 'ой'
                    result['surname_vp'] = surname[:-2] + 'ую'
                    result['surname_tp'] = surname[:-2] + 'ой'
                    result['surname_pp'] = surname[:-2] + 'ой'

        elif surname.endswith('а') and len(surname) > 2:
            if surname[-2] in 'гкх':
                result['surname_rp'] = surname[:-1] + 'и'
                result['surname_dp'] = surname[:-1] + 'е'
                result['surname_vp'] = surname[:-1] + 'у'
                result['surname_tp'] = surname[:-1] + 'ой'
                result['surname_pp'] = surname[:-1] + 'е'
            elif surname[-2] in consonant:
                result['surname_rp'] = surname[:-1] + 'ы'
                result['surname_dp'] = surname[:-1] + 'е'
                result['surname_vp'] = surname[:-1] + 'у'
                result['surname_tp'] = surname[:-1] + 'ой'
                result['surname_pp'] = surname[:-1] + 'е'

        elif surname.endswith('я'):
            result['surname_rp'] = surname[:-1] + 'и'
            result['surname_vp'] = surname[:-1] + 'ю'
            result['surname_tp'] = surname[:-1] + 'ей'
            if surname.endswith('ия'):
                result['surname_dp'] = surname[:-1] + 'и'
                result['surname_pp'] = surname[:-1] + 'и'
            else:
                result['surname_dp'] = surname[:-1] + 'е'
                result['surname_pp'] = surname[:-1] + 'е'

        elif surname.endswith('й') or surname.endswith('ь'):
            result['surname_rp'] = surname[:-1] + 'я'
            result['surname_dp'] = surname[:-1] + 'ю'
            result['surname_vp'] = surname[:-1] + 'я'
            result['surname_tp'] = surname[:-1] + 'ем'
            result['surname_pp'] = surname[:-1] + 'е'

        elif len(surname) > 1 and surname[-1] in consonant:
            result['surname_rp'] = surname + 'а'
            result['surname_dp'] = surname + 'у'
            result['surname_vp'] = surname + 'а'
            result['surname_tp'] = surname + 'ом'
            result['surname_pp'] = surname + 'е'

        return result
