from orm import Database, Model, IntegerField, TextField


# Объявляем модель данных, наследуясь от нашей ORM
class Student(Model):
    id = IntegerField(primary_key=True)
    name = TextField(nullable=False)
    age = IntegerField()
    faculty = TextField()


def main():
    # 1. Подключаемся к базе данных в оперативной памяти (чистится при закрытии)
    Database.connect(":memory:")

    # Создаем таблицу на основе структуры класса Student
    Student.create_table()
    print("=== Шаг 1: База данных и таблица 'students' успешно инициализированы ===")

    # 2. Создание записей (INSERT)
    student_1 = Student(name="Иван Петров", age=20, faculty="ИВТС")
    student_1.save()

    student_2 = Student(name="Анна Сидорова", age=19, faculty="ФКТТИ")
    student_2.save()

    student_3 = Student(name="Кирилл Федоров", age=22, faculty="ИВТС")
    student_3.save()
    print(f"Записи сохранены. Сгенерирован ID для Ивана: {student_1.id}, для Анны: {student_2.id}\n")

    # 3. Чтение записей с фильтрацией (SELECT + WHERE)
    print("=== Шаг 2: Выборка студентов факультета 'ИВТС' ===")
    ivts_students = Student.select().where(faculty="ИВТС").execute()
    for student in ivts_students:
        print(f"Студент: {student.name}, Возраст: {student.age} (ID: {student.id})")
    print()

    # 4. Обновление записи (UPDATE)
    print("=== Шаг 3: Обновление данных (День рождения Анны) ===")
    # Находим Анну по ID. Метод execute() возвращает список, берем первый элемент [0]
    anna = Student.select().where(id=2).execute()[0]
    print(f"Текущий возраст Анны в БД: {anna.age}")

    # Меняем возраст и отправляем апдейт в базу данных
    anna.age = 20
    anna.save()

    # Достаем из БД заново, чтобы убедиться в сохранении
    updated_anna = Student.select().where(id=2).execute()[0]
    print(f"Новый возраст Анны, перечитанный из БД: {updated_anna.age}\n")

    # 5. Удаление записи (DELETE)
    print("=== Шаг 4: Тестирование удаления записи ===")
    kirill = Student.select().where(id=3).execute()[0]
    kirill.delete()

    # Считаем количество оставшихся записей в таблице
    all_students = Student.select().execute()
    print(f"Кирилл удален. Общее число студентов в базе данных: {len(all_students)}")


if __name__ == "__main__":
    main()
