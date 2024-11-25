from typing import Any

from enum import Enum

class BookStatus(Enum):
    AVAILABLE = "в наличии"
    ISSUED = "выдана"
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class Book:
    """ 
        Класс описывает книгу в библиотеке.
    """
    def __init__(self, title: str, author: str, year: int):
        self._id = None
        self._status = BookStatus.AVAILABLE
        self.title = title
        self.author = author
        self.year = year
    
    @property
    def id(self) -> int | None:
        """
            Возвращение Id книги.
        """
        return self._id
    
    @id.setter
    def id(self, value: int) -> None:
        """
            Установка значения Id книги, если оно не задано.
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
        """
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        """
            Установка статуса книги.
        """
        if value not in ["в наличии", "выдана"]:
            raise ValueError("Неверное значение для статуса книги. Допустимые значения: 'в наличии' или 'выдана'.")
        self._status = value
    
    def __str__(self) -> str:
        """
            Строковое представление объекта книги.
        """
        return f"Книга: {self.title}, автор: {self.author}, год издания: {self.year}, статус: {self.status}"
    
    def __repr__(self):
        return f"{self._id}, {self.title}, {self.author}, {self.year}, {self._status}"
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'Book':
        """
            Создание объекта книги из словаря.
        """
        book = Book(data["title"], data["author"], data["year"])
        book.id = data["id"]
        book.status = data["status"]
        return book