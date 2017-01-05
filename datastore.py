from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

import book
from book import Book


engine = create_engine('sqlite:///book_wishlist.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def setup():
    ''' setup tasks here, if needed '''
    pass  # used in the future?


def shutdown():
    '''Any DB shutdown/cleanup tasks can go here'''
    session.close()


def get_books(**kwargs):
    ''' Return books from DB. With no arguments, returns everything. '''

    if kwargs == None:
        all_books = session.query(Book).all()
        return all_books

    read = kwargs['read']

    if read is not None:
        all_books = session.query(Book).filter_by(read=read).all()
        return all_books


def add_book(book):
    ''' Add to db, set id value'''

    session.add(book)   # Book will be updated with id from database.
    session.commit()


def set_read(book_id, read):
    '''Update book with given book_id to read. Return True if book is found in DB and update is made, False otherwise.'''

    try:
        book = session.query(Book).filter_by(id=book_id).one()
        book.read = read
        session.commit()  # Save modified Book object

        return True

    except NoResultFound as e:
        #book not found
        print(e)
        return False

    # Other errors - multiple rows found - let error be thrown, design issue permitting more than one book with same primary key.
