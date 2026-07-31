# Mini ORM

[🇬🇧 English](README.md) | [🇷🇺 Русский](README.ru.md)

Небольшая ORM на Python поверх SQLite, реализованная с нуля: метаклассы, дескрипторы полей и query builder.

## Возможности
- Описание моделей через классы (`class Student(Model): ...`)
- Поля `IntegerField`, `TextField` с поддержкой `primary_key` и `nullable`
- Автосоздание таблицы по структуре модели (`Model.create_table()`)
- CRUD-операции: `save()`, `delete()`
- Выборка с фильтрацией: `Model.select().where(...).execute()`

## Стек
- Python 3
- sqlite3 (стандартная библиотека)

## Структура
```
orm/
├── database.py     # подключение к SQLite, курсор, коммит
├── fields.py        # дескрипторы полей (IntegerField, TextField)
├── metaclasses.py   # метакласс, собирающий поля модели
├── models.py         # базовый класс Model (create_table, save, delete)
└── query.py          # query builder (select/where/execute)
main.py               # пример использования
```

## Запуск
```bash
python main.py
```
Демонстрирует создание таблицы, вставку записей, выборку с фильтром, обновление и удаление — всё на базе в оперативной памяти (`:memory:`).

## Пример
```python
class Student(Model):
    id = IntegerField(primary_key=True)
    name = TextField(nullable=False)
    age = IntegerField()
    faculty = TextField()

Database.connect(":memory:")
Student.create_table()

student = Student(name="Иван Петров", age=20, faculty="ИВТС")
student.save()

ivts_students = Student.select().where(faculty="ИВТС").execute()
```

## Лицензия
MIT
