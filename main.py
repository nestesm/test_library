from library import Library
from book import BookStatus

def main():
    library = Library()
    library.load_data()
    
    while True:
        print("\n Библиотека:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")
        
        action = input("Выберите действие: ").strip()
        match action:
            case "1":
                title = input("Введите название книги: ").strip()
                author = input("Введите название книги: ").strip()
                try:
                    year = int(input("Введите год издания книги: ").strip())
                    library.add_book(title, author, year)
                except ValueError:
                    print("Некорректный год издания.")
                    continue
                
            case "2":
                try:
                    book_id = int(input("Введите Id книги: ").strip())
                    if library.remove_book(book_id):
                        print("Книга удалена.")
                    else:
                        print("Книга не найдена.")
                except ValueError:
                    print("Некорректный Id книги.")
                    continue
            case "3":
                pass
            case "4":
                books = library.books
                if books:
                    print("Книги в библиотеке:")
                    for book in books:
                        print(book)
                else:
                    print("В библиотеке нет книг.")
            case "5":
                try:
                    book_id = int(input("Введите Id книги: ").strip())
                    status = input("Введите статус книги: ").strip()
                    if not library.update_book_status(book_id, status):
                        print(f"Ошибка обновления статуса книги. Проверьте введенные данные - Id или статус.\n 
                              Допустимые значения для статуса: {BookStatus.list()}")
                except ValueError:
                    print("Некорректный Id книги.")
                    continue
            case "0":
                print("Окончание работы.")
                break
            case _:
                print("Некорректное действие.")
                
        


if __name__ == '__main__':
    main()