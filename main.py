from library import Library
from book import BookStatus

def main():
    """
        Основная функция работы с библиотекой.

        Создаёт объект библиотеки, загружает данные из файла и предоставляет
        пользователю меню для управления библиотекой.
    """
    library = Library() # Создаём объект библиотеки
    library.load_data() # Загружаем данные из файла
    while True:
        print("\n Библиотека:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")
        
        action = input("Выберите действие: ").strip() # Получаем действие от пользователя
        match action: # Обработка действий 
            case "1": # Добавление книги
                title = input("Введите название книги: ").strip()
                author = input("Введите название книги: ").strip()
                try: # Проверяем корректность года издания
                    year = int(input("Введите год издания книги: ").strip()) 
                    library.add_book(title, author, year)
                except ValueError:
                    print("Некорректный год издания.")
                    continue
                
            case "2": # Удаление книги
                try:
                    book_id = int(input("Введите Id книги: ").strip())
                    if library.remove_book(book_id):
                        print("Книга удалена.")
                    else:
                        print("Книга не найдена.")
                except ValueError:
                    print("Некорректный Id книги.")
                    continue
            case "3": # Поиск книг
                field = input("Введите название поля для поиска? (title/author/year): ").strip().lower()
                if field not in ["title", "author", "year"]:
                    print("Ошибка: поле для поиска должно быть 'title', 'author' или 'year'.")
                    continue
                data = input("Введите данные для поиска: ").strip()
                results = library.search_books(data, field)
                if results:
                    print("Найденные книги:")
                    for book in results:
                        print(book)
                else:
                    print("Книг по вашему запросу не найдено.")
                
                pass
            case "4": # Показ всех книг
                books = library.books
                if books:
                    print("Книги в библиотеке:")
                    for book in books:
                        print(book)
                else:
                    print("В библиотеке нет книг.")
            case "5": # Изменение статуса книги
                try:
                    book_id = int(input("Введите Id книги: ").strip())
                    status = input("Введите статус книги: ").strip()
                    if not library.update_book_status(book_id, status):
                        print(f"Ошибка обновления статуса книги. Проверьте введенные данные - Id или статус.\n 
                              Допустимые значения для статуса: {', '.join(BookStatus.list())}")
                except ValueError:
                    print("Некорректный Id книги.")
                    continue
            case "0": # Завершение работы программы
                print("Окончание работы.")
                break
            case _: # Некорректный ввод действия
                print("Некорректное действие.")
                
        


if __name__ == '__main__':
    main()