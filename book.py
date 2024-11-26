from typing import Any, Optional, List

from enum import Enum

class BookStatus(Enum):
    """
        Перечисление для статусов книги.
    """
    AVAILABLE = "в наличии"
    ISSUED = "выдана"
    
    @classmethod
    def list(cls) -> List[str]:
        """
            Возвращает список всех значений перечисления.

            Returns:
                list[str]: Список значений статусов книги.
        """
        return list(map(lambda c: c.value, cls))
    
    

class Book:
    """ 
        Класс описывает книгу в библиотеке.
        
        Атрибуты:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            _id (Optional[int]): Уникальный идентификатор книги (задаётся автоматически).
            _status (BookStatus): Статус книги (по умолчанию AVAILABLE).

    """
    def __init__(self, title: str, author: str, year: int):
        self._id: Optional[int] = None 
        self._status = BookStatus.AVAILABLE
        self.title: str = title
        self.author: str = author
        self.year: int = year
    
    @property
    def id(self) -> Optional[int]:
        """
            Возвращение Id книги.
            
            Returns:
                Optional[int]: Уникальный идентификатор книги или None, если не установлен.
        """
        return self._id
    
    @id.setter
    def id(self, value: int) -> None:
        """
            Установка значения Id книги, если оно не задано.
            
            Args:
                value (int): Значение для ID.

            Raises:
                AttributeError: Если Id уже установлен.
                ValueError: Если значение Id некорректное.
        """
        if self._id is not None:
            raise AttributeError("Id книги установлен, изменение невозможно.")
        if not isinstance(value, int) or value < 0:
            raise ValueError("Некорректное значение для id книги.") 
        self._id = value
        
    @property
    def status(self) -> str:
        """
            Возвращение статуса книги.
            
            Returns:
                BookStatus: Текущий статус книги.
        """
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        """
            Установка статуса книги.
            
            Args:
                value (str): Новый статус книги. Можно указать строку 
                                      или объект BookStatus.

            Raises:
                ValueError: Если передано некорректное строковое значение.
                TypeError: Если тип аргумента не поддерживается.
        """
        if isinstance(value, str):
            try:
                value = BookStatus(value)  # Преобразуем строку в объект BookStatus
            except ValueError:
                raise ValueError(f"Неверное значение для статуса книги. Допустимые значения: {', '.join(BookStatus.list())}") 
        if not isinstance(value, BookStatus):
            raise ValueError(f"Неверное значение для статуса книги. Допустимые значения: {', '.join(BookStatus.list())}.")
        self._status = value
    
    def __str__(self) -> str:
        """
            Строковое представление объекта книги.
            
            Returns:
                str: Информация о книге в текстовом формате.
        """
        return f"Книга: {self.title}, автор: {self.author}, год издания: {self.year}, статус: {self.status}"
    
    def to_dict(self) -> dict[str, Any]:
        """
            Преобразование объекта книги в словарь.
            
            Returns:
                dict[str, Any]: Словарь с данными книги.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value
        }
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'Book':
        """
            Создание объекта книги из словаря.
            
            Args:
                data (dict[str, Any]): Словарь с данными книги.

            Returns:
                Book: Новый объект книги.

            Raises:
                KeyError: Если в словаре отсутствуют обязательные ключи.
                ValueError: Если данные содержат некорректные значения.
        """
        book = Book(data["title"], data["author"], data["year"])
        book.id = data.get("id") # Устанавливаем ID, если он есть
        book.status = data.get("status", BookStatus.AVAILABLE.value) # Устанавливаем статус
        return book