from orm.database import Database

class Query:
    def __init__(self, model_class):
        self.model_class = model_class
        self.where_conditions = []
        self.where_params = []

    def where(self, **kwargs):
        """Добавляет условия фильтрации (например, age=20)"""
        for key, value in kwargs.items():
            if key in self.model_class._fields:
                self.where_conditions.append(f"{key} = ?")
                self.where_params.append(value)
            else:
                raise AttributeError(f"Модель '{self.model_class.__name__}' не содержит поля '{key}'")
        return self

    def execute(self):
        """Выполняет сгенерированный SQL-запрос и возвращает список объектов модели"""
        cursor = Database.get_cursor()
        sql = f"SELECT * FROM {self.model_class._table_name}"

        if self.where_conditions:
            sql += " WHERE " + " AND ".join(self.where_conditions)

        cursor.execute(sql, self.where_params)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            # Создаем пустой объект модели и наполняем его данными из БД
            obj = self.model_class()
            for key in self.model_class._fields.keys():
                obj.__dict__[key] = row[key]
            results.append(obj)
        return results
