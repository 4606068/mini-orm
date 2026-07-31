import sqlite3

class Database:
    _connection = None

    @classmethod
    def connect(cls, db_name):
        """Устанавливает соединение с файлом базы данных или :memory:"""
        cls._connection = sqlite3.connect(db_name)
        # Позволяет обращаться к полям строки по именам, как в словаре
        cls._connection.row_factory = sqlite3.Row

    @classmethod
    def get_cursor(cls):
        """Возвращает активный курсор для выполнения SQL-запросов"""
        if cls._connection is None:
            raise RuntimeError("База данных не подключена. Сначала вызовите Database.connect()")
        return cls._connection.cursor()

    @classmethod
    def commit(cls):
        """Фиксирует текущую транзакцию в базе данных"""
        if cls._connection:
            cls._connection.commit()
