import unittest
import wishlist
from wishlist import datastore, book
from wishlist.book import Book

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDataStore(unittest.TestCase):

    test_db = 'sqlite:///test_database.db'

    ''' Will run before each test. Create brand new database '''
    def setUp(self):
        datastore.engine = create_engine(self.test_db, echo=False)
        datastore.Session = sessionmaker(bind=datastore.engine)
        datastore.session = datastore.Session()
        self.session = datastore.session
        book.Base.metadata.create_all(datastore.engine)


    ''' Drop tables to wipe database; so that any subsequent tests can start with new database '''
    def tearDown(self):
        book.Base.metadata.drop_all(datastore.engine)
        datastore.session.close()


    def test_get_books_no_args(self):

        self.add_example_books()
        results = datastore.get_books()  # Expect all books to be returned
        # assertCountEqual checks if two lists have the same elements, regardless of order.
        self.assertCountEqual(results, self.test_books)

    def test_get_books_read_or_not_read(self):

        self.add_example_books()

        results = datastore.get_books(read=True)
        read_books = [ b for b in self.test_books if b.read ]
        self.assertCountEqual(read_books, results)

        results = datastore.get_books(read=False)
        read_books = [ b for b in self.test_books if not b.read ]
        self.assertCountEqual(read_books, results)


    def test_add_book(self):

        book1 = Book('1984', 'George Orwell')
        datastore.add_book(book1)

        # Query db for all Book objects. Expect a list of one object, [ book ]
        results = self.session.query(Book).all()
        self.assertEqual( [ book1 ] , results)

        # And add another book
        book2 = Book('Python Data Science Handbook', 'Jake VanderPlas', read=True)
        datastore.add_book(book2)

        # Query db for all Book objects. Expect a list of one object, [ book ]
        results = self.session.query(Book).all()
        self.assertCountEqual( [ book1, book2 ] , results)



    def test_set_read_books_exist(self):

        self.add_example_books()

        # set_read should return True if book is found and updated.

        # mark a read book as unread
        read_book = self.test_books[0]
        self.assertTrue(datastore.set_read(read_book.id, False))
        self.assertFalse(read_book.read)

        # mark a read book as read
        read_book_2 = self.test_books[2]
        self.assertTrue(datastore.set_read(read_book.id, True))
        self.assertTrue(read_book.read)

        # mark an unread book as unread
        unread_book = self.test_books[2]
        self.assertTrue(datastore.set_read(read_book.id, False))
        self.assertFalse(read_book.read)

        # mark an unread book as read
        unread_book_2 = self.test_books[3]
        self.assertTrue(datastore.set_read(read_book.id, True))
        self.assertTrue(read_book.read)


    def test_set_read_book_nonexistant_book(self):

        self.add_example_books()

        self.assertFalse(datastore.set_read(100, True))
        self.assertFalse(datastore.set_read(100, False))


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


if __name__ == '__main__':
    unittest.main()
