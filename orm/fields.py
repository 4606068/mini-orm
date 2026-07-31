class Field:
    def __init__(self, primary_key=False, nullable=True):
        self.primary_key = primary_key
        self.nullable = nullable
        self.name = None  # Имя поля автоматически заполнит метакласс

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not self.nullable and value is None and not self.primary_key:
            raise ValueError(f"Поле '{self.name}' не может иметь значение None (NOT NULL constraint)")
        instance.__dict__[self.name] = value


class IntegerField(Field):
    def get_sql_type(self):
        sql = "INTEGER"
        if self.primary_key:
            sql += " PRIMARY KEY AUTOINCREMENT"
        return sql


class TextField(Field):
    def get_sql_type(self):
        sql = "TEXT"
        if not self.nullable:
            sql += " NOT NULL"
        return sql
