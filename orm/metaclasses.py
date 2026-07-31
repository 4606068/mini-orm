from orm.fields import Field

class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        # Не обрабатываем базовый класс Model
        if name == "Model":
            return super().__new__(mcs, name, bases, attrs)

        fields = {}
        primary_key_name = None

        # Ищем все атрибуты, которые являются наследниками Field
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                value.name = key
                fields[key] = value
                if value.primary_key:
                    if primary_key_name:
                        raise TypeError(f"У модели {name} может быть только один первичный ключ.")
                    primary_key_name = key
                attrs.pop(key)  # Удаляем из стандартных атрибутов класса

        # Добавляем служебные атрибуты во вновь создаваемый класс
        attrs["_fields"] = fields
        attrs["_table_name"] = name.lower() + "s"  # Имя таблицы во множественном числе
        attrs["_primary_key"] = primary_key_name

        return super().__new__(mcs, name, bases, attrs)
