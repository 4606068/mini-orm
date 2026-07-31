# Mini ORM

[🇬🇧 English](README.md) | [🇷🇺 Русский](README.ru.md)

A small Python ORM built on top of SQLite from scratch: metaclasses, field descriptors, and a query builder.

## Features
- Define models as plain classes (`class Student(Model): ...`)
- `IntegerField`, `TextField` with `primary_key` / `nullable` support
- Auto table creation based on model structure (`Model.create_table()`)
- CRUD operations: `save()`, `delete()`
- Filtered queries: `Model.select().where(...).execute()`

## Tech stack
- Python 3
- sqlite3 (standard library)

## Structure
```
orm/
├── database.py     # SQLite connection, cursor, commit
├── fields.py        # field descriptors (IntegerField, TextField)
├── metaclasses.py   # metaclass that collects model fields
├── models.py         # base Model class (create_table, save, delete)
└── query.py          # query builder (select/where/execute)
main.py               # usage example
```

## Run
```bash
python main.py
```
Demonstrates table creation, inserting records, filtered selects, updating, and deleting — all on an in-memory database (`:memory:`).

## Example
```python
class Student(Model):
    id = IntegerField(primary_key=True)
    name = TextField(nullable=False)
    age = IntegerField()
    faculty = TextField()

Database.connect(":memory:")
Student.create_table()

student = Student(name="John Doe", age=20, faculty="CS")
student.save()

cs_students = Student.select().where(faculty="CS").execute()
```

## License
MIT
