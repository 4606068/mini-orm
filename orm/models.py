from orm.database import Database
from orm.metaclasses import ModelMetaclass
from orm.query import Query

class Model(metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._fields:
                setattr(self, key, value)
            else:
                raise AttributeError(f"Неизвестное поле '{key}' для модели {self.__class__.__name__}")

        # Гарантируем наличие поля первичного ключа в объекте
        if self._primary_key and self._primary_key not in kwargs:
            setattr(self, self._primary_key, None)

    @classmethod
    def create_table(cls):
        """Генерирует DDL SQL-запрос на создание таблицы на основе полей класса"""
        cursor = Database.get_cursor()
        field_definitions = []

        for name, field in cls._fields.items():
            field_definitions.append(f"{name} {field.get_sql_type()}")

        sql = f"CREATE TABLE IF NOT EXISTS {cls._table_name} ({', '.join(field_definitions)});"
        cursor.execute(sql)
        Database.commit()

    def save(self):
        """Автоматически определяет INSERT или UPDATE операцию и синхронизирует объект с БД"""
        cursor = Database.get_cursor()
        pk = self._primary_key
        pk_value = getattr(self, pk) if pk else None

        # Собираем все заполненные поля, кроме автоинкрементного ID (если он еще пуст)
        fields_to_save = {
            k: getattr(self, k)
            for k in self._fields
            if k != pk or getattr(self, k) is not None
        }

        if pk_value is None:
            # Объект новый — делаем INSERT
            columns = ", ".join(fields_to_save.keys())
            placeholders = ", ".join(["?"] * len(fields_to_save))
            sql = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders});"
            cursor.execute(sql, list(fields_to_save.values()))
            if pk:
                setattr(self, pk, cursor.lastrowid)  # Записываем сгенерированный базой ID
        else:
            # Объект уже существует — делаем UPDATE
            set_clause = ", ".join([f"{k} = ?" for k in fields_to_save.keys()])
            sql = f"UPDATE {self._table_name} SET {set_clause} WHERE {pk} = ?;"
            params = list(fields_to_save.values()) + [pk_value]
            cursor.execute(sql, params)

        Database.commit()

    def delete(self):
        """Удаляет запись текущего объекта из базы данных"""
        pk = self._primary_key
        pk_value = getattr(self, pk)
        if not pk or pk_value is None:
            raise ValueError("Невозможно удалить объект, которого нет в базе данных (отсутствует ID)")

        cursor = Database.get_cursor()
        sql = f"DELETE FROM {self._table_name} WHERE {pk} = ?;"
        cursor.execute(sql, (pk_value,))
        Database.commit()
        setattr(self, pk, None)  # Сбрасываем ID удаленного объекта

    @classmethod
    def select(cls):
        """Инициализирует построитель запросов для текущего класса модели"""
        return Query(cls)
