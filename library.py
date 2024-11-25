import json

from book import Book, BookStatus

class Library:
    """ 
        Класс описывает возможное взаимодействие с библиотекой.
    """
    def __init__(self, file_path: str = "data.json"):
        self.books: list[Book] = []
        self.file_path = file_path
        
    def load_data(self) -> None:
        """
            Загрузка данных-книг из файла.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []
            
    def save_data(self) -> None:
        """
            Выгрузка данных в файл.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([repr(book) for book in self.books], file, sort_keys=True, indent=4, ensure_ascii=False)
            
    def add_book(self, title: str, author: str, year: int) -> Book:
        """
            Добавление книги в библиотеку и в файл.
        """
        new_book = Book(title, author, year)
        new_book.id = len(self.books) + 1
        self.books.append(new_book)
        self.save_data()
        return new_book
    
    def remove_book(self, book_id: int) -> None:
        """
            Удаление книги из библиотеки и файла.
        """
        pass
    
    def update_book_status(self, book_id: int, status: str) -> None:
        """
            Изменение статуса книги.
        """
        if status not in BookStatus.list():
            return False
        for book in self.books:
            if book_id == book.id:
                book.status = status
                self.save_data()
                return True
        return False
        
   
    
    