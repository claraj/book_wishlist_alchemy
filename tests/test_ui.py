import unittest
from unittest.mock import patch

import wishlist.book

from wishlist.book import Book
from wishlist import ui

class TestUI(unittest.TestCase):

    @patch('builtins.print')
    def test_show_list(self, mock_print):

        book1 = Book("King Lear", "Shakespeare", True)
        book2 = Book("The Cat in the Hat", "Dr. Seuss", True)
        book3 = Book("Swimming to Antarctica", "Lynne Cox", False)

        books = [ book1, book2, book3 ]

        ui.show_list(books)

        # This one is tricky - how do you test that read and not read are being displayed correctly?
        # And, what if there are extra print statements before the book list?
        # Let's assume that the first print statements include the names and titles are printed in order

        for test_book, print_call_args in zip(books, mock_print.call_args_list):
            printed_text = print_call_args[0][0]
            self.assertEqual(test_book, printed_text)  # Use this if printing a book object
            # self.assertTrue(test_book.title in printed_text)  # Use this if print called with a string, to look for text
            # self.assertTrue(test_book.author in printed_text)


    @patch('builtins.input')
    def test_ask_for_book_id(self, mock_input):
        # Test with valid
        mock_input.side_effect = [ '10' ]
        b_id = ui.ask_for_book_id()
        self.assertEqual(10, b_id)

        # Invalid inputs, followed by a valid. Function should return 3
        mock_input.side_effect = [ '-1', 'pizza', '-100', 'abc', 'abc123', '3']
        b_id = ui.ask_for_book_id()
        self.assertEqual(3, b_id)


    @patch('builtins.input', side_effect=['1984', 'George Orwell'])
    def test_get_new_book_info(self, mock_input):

        book_created = ui.get_new_book_info()
        self.assertEqual('1984', book_created.title)
        self.assertEqual('George Orwell', book_created.author)
        self.assertEqual(False, book_created.read)
        self.assertIsNone(book_created.id)


if __name__ == '__main__':
    unittest.main()
