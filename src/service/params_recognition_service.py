import spacy
import re
from service.subjects_service import SubjectsService
from src.service.names_service import NamesService
from src.service.surnames_service import SurnamesService
from src.entities.name import Name
from src.entities.surname import Surname


class ParamsService:
    def __init__(self):
        self.processor = spacy.load('ru_core_news_md')
        self.ruler = self.processor.add_pipe("entity_ruler")
        self.ruler.add_patterns([
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]+\.[0-9]+'}}], 'id': '1'},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'январь'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'февраль'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'март'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'апрель'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'май'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'июнь'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'июль'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'август'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'сентябрь'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'октябрь'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'ноябрь'}]},
            {'label': 'DATE', 'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}, {'LEMMA': 'декабрь'}]},
            {'label': 'NUM',  'pattern': [
                {'TEXT': {'REGEX': '[0-9]'}}], 'id': '2'},
        ])
        self.names_service = NamesService()
        self.surnames_service = SurnamesService()
        self.subjects_service = SubjectsService()

    @staticmethod
    def prepare(query: str):
        return re.sub(
            r'\s+',
            ' ',
            re.sub(
                r'[!\"\#$%&\'()*+\-./:;<= >?@\[\\\]^_‘{|}~]',
                ' ',
                query.lower().replace('ё', 'е')
            )
        ).title()

    def get_names_surnames(self, sentence: str) -> tuple[list[tuple[str, Name]], list[tuple[str, Surname]]]:
        """
        Предложение на входе должно быть лемматизированным!!!
        """
        names: list[tuple[str, Name]] = []
        surnames: list[tuple[str, Surname]] = []
        for word in sentence.split():
            potential_names = self.names_service.get_by_name_any_case(word)
            for name in potential_names:
                names.append((word, name))
            potential_surnames = self.surnames_service.get_by_surname_any_case(
                word)
            for surname in potential_surnames:
                surnames.append((word, surname))

        return names, surnames

    def get_params(self, query: str) -> tuple[dict[str, str | list[str]], str]:
        result = dict()
        doc = self.processor(query)
        for ent in doc.ents:
            if ent.label_ == 'NUM' or ent.label_ == 'DATE':
                result[ent.label_] = ent.text

        query_prepared = self.prepare(query)
        names, surnames = self.get_names_surnames(query_prepared)
        res_query = query_prepared

        valid = []

        for name, name_from_db in names:
            for surname, surname_from_db in surnames:
                if (name + ' ' + surname in query_prepared or
                        surname + ' ' + name in query_prepared):

                    res_query = res_query.replace(name, '')
                    res_query = res_query.replace(surname, '')

                    valid.append(
                        {
                            'name': name_from_db.name_ip,
                            'surname': surname_from_db.surname_ip
                        }
                    )

        if not valid:
            for surname, surname_from_db in surnames:
                if surname in query_prepared:

                    res_query = res_query.replace(surname, '')

                    valid.append(
                        {
                            'surname': surname_from_db.surname_ip
                        }
                    )

        if valid:
            result['PER'] = valid

        doc = self.processor(res_query)
        lemmatized = ' '.join(token.lemma_ for token in doc)
        res_query = ''

        for subject in self.subjects_service.get():
            for idx, lemma in enumerate([token.lemma_ for token in doc]):
                if subject.acronym.lower() == lemma:
                    result['SUBJ'] = subject.subject
                elif subject.lemma in lemmatized and lemma in subject.lemma.split():
                    result['SUBJ'] = subject.subject
                    res_query = (
                        ' '.join(str(token) for token in doc[:idx]) +
                        ' '.join(
                            str(token) for token in doc[idx + (len(subject.lemma.split(' '))):])
                    )
                    break
                else:
                    res_query = res_query + str(doc[idx]) + ' '

        return result, re.sub(r'\s+', ' ', res_query).strip().capitalize()
