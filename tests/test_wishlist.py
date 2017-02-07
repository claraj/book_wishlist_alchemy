import unittest
import main
import wishlist
#from .. import main
from wishlist import book, datastore, ui
from wishlist.book import Book

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from unittest.mock import patch

class TestWishlist(unittest.TestCase):

    test_db = 'sqlite:///test_database.db'

    ''' Will run before each test. Create brand new database '''
    def setUp(self):
        datastore.engine = create_engine(self.test_db, echo=False)
        datastore.Session = sessionmaker(bind=datastore.engine)
        datastore.session = datastore.Session()
        self.session = datastore.session
        book.Base.metadata.create_all(datastore.engine)

    ''' Will run after each test. Drop tables to wipe database; so that any subsequent tests can start with new database '''
    def tearDown(self):
        book.Base.metadata.drop_all(datastore.engine)
        datastore.session.close()

    # Tests for show_read and show_unread omitted

    @patch('builtins.input')
    @patch('wishlist.ui.message')
    def test_mark_book_read(self, mock_message, mock_input):
        self.add_example_books()

        # Check that book that exists and is unread is updated
        mock_input.return_value = 3  # Book id = 3
        main.book_read()
        mock_message.assert_called_with('Successfully updated')
        book3 = self.session.query(Book).filter_by(id=3).one_or_none()
        self.assertTrue(book3.read)

        # Check that book that doesn't exist is not updated
        mock_input.return_value = 30  # Book id = 30
        main.book_read()
        mock_message.assert_called_with('Book id not found in database')


    @patch('builtins.input', side_effect=['1984', 'George Orwell', 'Brave New World', 'Aldous Huxley'])
    @patch('wishlist.ui.message')
    def test_new_book(self, mock_message, mock_input):

        # Add book
        main.new_book()
        # Check book is in db - should be the only book in the db.
        last_call_arg = mock_message.call_args_list[0][0][0]
        book_added = 'Book added' in last_call_arg
        self.assertTrue(book_added)

        books_from_db = self.session.query(Book).all()
        self.assertEqual(1, len(books_from_db))
        self.assertEqual('1984', books_from_db[0].title)
        self.assertEqual('George Orwell', books_from_db[0].author)


        # Add another book
        main.new_book()
        # Check this book is also in db - should be the only book in the db.
        last_call_arg = mock_message.call_args_list[0][0][0]
        book_added = 'Book added' in last_call_arg
        self.assertTrue(book_added)

        books_from_db = self.session.query(Book).all()

        self.assertEqual(2, len(books_from_db))


        # Should have one book representing 1984
        # And another for Brave New World.

        # Find 1984, assert data is correct, remove from result list
        for b in books_from_db:
            if b.title == '1984':
                self.assertEqual('George Orwell', b.author)
                self.assertFalse(b.read)
                books_from_db.remove(b)
                break

        # Find 1984, assert data is correct, remove from result list
        for b in books_from_db:
            if b.title == 'Brave New World':
                self.assertEqual('Aldous Huxley', b.author)
                self.assertFalse(b.read)
                books_from_db.remove(b)
                break

        self.assertEqual(0, len(books_from_db))



    def add_example_books(self):

        book1 = Book("King Lear", "Shakespeare", True)
        book2 = Book("The Cat in the Hat", "Dr. Seuss", True)
        book3 = Book("Brave New World", "Aldous Huxley", False)
        book4 = Book("Swimming to Antarctica", "Lynne Cox", False)
        book5 = Book("High Fidelity", "Nick Hornby", True)
        book6 = Book("Trainspotting", "Irvine Welsh", False)

        self.test_books = [ book1, book2, book3, book4, book5, book6 ]
        datastore.session.add_all(self.test_books)

        self.session.commit()
