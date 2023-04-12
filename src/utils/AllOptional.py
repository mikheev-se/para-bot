import pydantic


class AllOptional(pydantic.main.ModelMetaclass):
    """
    Делает все поля класса опциональными
    Используется для автоматизации создание DTO на обновление
    """
    def __new__(cls, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})

        for base in bases:
            for base_ in base.__mro__:
                if base_ is pydantic.BaseModel:
                    break
                annotations.update(base_.__annotations__)

        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = annotations[field] | None
        namespaces['__annotations__'] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)
