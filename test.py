import unittest
import os
from pathlib import Path

from library import Library
from book import Book, BookStatus

# Подключаем тестируемые классы
class TestBook(unittest.TestCase):
    """Тесты для класса Book."""

    def test_create_book(self):
        """Тест создания книги и проверки её полей."""
        book = Book("Преступление и наказание", "Фёдор Достоевский", 1866)
        self.assertEqual(book.title, "Преступление и наказание")
        self.assertEqual(book.author, "Фёдор Достоевский")
        self.assertEqual(book.year, 1866)
        self.assertEqual(book.status.value, BookStatus.AVAILABLE.value)

    def test_set_book_id(self):
        """Тест установки id книги."""
        book = Book("Мастер и Маргарита", "Михаил Булгаков", 1966)
        book.id = 1
        self.assertEqual(book.id, 1)
        with self.assertRaises(AttributeError):
            book.id = 2  # Повторная установка id должна вызвать ошибку

    def test_change_status(self):
        """Тест изменения статуса книги."""
        book = Book("1984", "Джордж Оруэлл", 1949)
        book.status = "выдана"
        self.assertEqual(book.status, BookStatus.ISSUED.value)
        with self.assertRaises(ValueError):
            book.status = "недоступна"  # Некорректное значение статуса

    def test_from_dict(self):
        """Тест создания книги из словаря."""
        data = {
            "id": 1,
            "title": "1984",
            "author": "Джордж Оруэлл",
            "year": 1949,
            "status": "в наличии",
        }
        book = Book.from_dict(data)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Джордж Оруэлл")
        self.assertEqual(book.year, 1949)
        self.assertEqual(book.status, "в наличии")


class TestLibrary(unittest.TestCase):
    """Тесты для класса Library."""

    def setUp(self):
        """Создаём тестовую библиотеку перед каждым тестом."""
        self.library = Library(file_path="test_data.json")
        self.library.books = []  # Очищаем библиотеку

    def tearDown(self):
        """Удаляем тестовый файл после каждого теста."""
        if Path(self.library.file_path).exists():
            os.remove(self.library.file_path)

    def test_add_book(self):
        """Тест добавления книги в библиотеку."""
        book = self.library.add_book("Преступление и наказание", "Фёдор Достоевский", 1866)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Преступление и наказание")
        self.assertEqual(self.library.books[0].author, "Фёдор Достоевский")
        self.assertEqual(self.library.books[0].year, 1866)

    def test_remove_book(self):
        """Тест удаления книги из библиотеки."""
        book = self.library.add_book("Преступление и наказание", "Фёдор Достоевский", 1866)
        self.assertTrue(self.library.remove_book(book.id))
        self.assertEqual(len(self.library.books), 0)
        self.assertFalse(self.library.remove_book(999))  # Несуществующий ID

    def test_update_book_status(self):
        """Тест изменения статуса книги."""
        book = self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.assertTrue(self.library.update_book_status(book.id, "выдана"))
        self.assertEqual(self.library.books[0].status, "выдана")
        self.assertFalse(self.library.update_book_status(book.id, "недоступна"))  # Некорректный статус

    def test_search_books(self):
        """Тест поиска книг по полю."""
        self.library.add_book("Преступление и наказание", "Фёдор Достоевский", 1866)
        self.library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1966)
        results = self.library.search_books("булгаков", "author")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Михаил Булгаков")

    def test_save_and_load_data(self):
        """Тест сохранения и загрузки данных."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.save_data()
        # Создаём новую библиотеку и загружаем данные
        new_library = Library(file_path="test_data.json")
        new_library.load_data()
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "1984")


if __name__ == "__main__":
    unittest.main()
