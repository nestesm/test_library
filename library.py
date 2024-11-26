import json
from pathlib import Path
from typing import List, Optional

from book import Book, BookStatus

class Library:
    """ 
        Класс описывает взаимодействие с библиотекой.
        
        Атрибуты:
            file_path (str): Путь к файлу с данными библиотеки.
            books (List[Book]): Список книг в библиотеке.
    """
    def __init__(self, file_path: str = "data.json"):
        """Инициализация библиотеки с файлом.

        Args:
            file_path (str): Путь к файлу для загрузки/сохранения данных библиотеки. 
                             По умолчанию "data.json".
        """
        
        self.books: List[Book] = []
        self.file_path = file_path 
        
    def load_data(self) -> None:
        """
            Загрузка данных-книг из файла.
            
            Если файл отсутствует или содержит некорректные данные, список книг 
            (`self.books`) будет пустым.   
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file) # Загружаем данные из файла
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = [] # Если файл отсутствует или некорректен, оставляем список пустым
            
    def save_data(self) -> None:
        """
            Выгрузка данных в файл.
            
            Директория создаётся автоматически, если отсутствует.
        """
        path = Path(self.file_path) # Создаём директорию, если её нет
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],  # Сохраняем список книг
                file,
                sort_keys=True, # Сортируем ключи для читаемости
                indent=4, # Форматируем JSON с отступами
                ensure_ascii=False # Оставляем символы Unicode
                )
            
    def add_book(self, title: str, author: str, year: int) -> Book:
        """
            Добавление книги в библиотеку и в файл.
            
            Args:
                title (str): Название книги.
                author (str): Автор книги.
                year (int): Год издания.

            Returns:
                Book: Экземпляр добавленной книги.
        """
        new_book = Book(title, author, year)
        new_book.id = len(self.books) + 1 # Устанавливаем уникальный ID
        self.books.append(new_book)
        self.save_data() # Сохраняем обновлённые данные
        return new_book
    
    def update_book_status(self, book_id: int, status: str) -> None:
        """
            Изменение статуса книги.
            
            Args:
                book_id (int): Уникальный идентификатор книги.
                status (str): Новый статус книги (должен быть допустимым).

            Returns:
                bool: True, если статус обновлён успешно; False, если книга или 
                    статус не найдены.
        """
        if status not in BookStatus.list(): # Проверяем допустимость статуса
            return False
        for book in self.books:
            if book_id == book.id: # Находим книгу по ID
                book.status = status # Обновляем статус
                self.save_data() # Сохраняем обновлённые данные
                return True
        return False
    
    def remove_book(self, book_id: int) -> bool:
        """
            Удаление книги из библиотеки и файла.
            
            Args:
                book_id (int): Уникальный идентификатор книги.
                
            Returns:
                bool: True, если книга удалена; False, если книга не найдена.
        """
        for book in self.books:
            if book_id == book.id:
                self.books.remove(book) # Удаляем кни
                self.save_data() # Сохраняем обновлённые данные
                return True
        return False
    
    def search_books(self, data: str, field: str) -> List[Book]:
        """
            Поиск книг по заданному полю.
            
            Args:
                data (str): Значение для поиска.
                field (str): Поле книги, по которому производится поиск.

            Returns:
                List[Book]: Список книг, соответствующих критерию поиска.
        """
        results = []
        for book in self.books: 
            value = getattr(book, field, None) # Получаем значение поля

            if value is not None and data in str(value).lower(): # Если значение существует, преобразуем его к строке и ищем совпадение
                results.append(book)

        return results
    
    
   
    
    