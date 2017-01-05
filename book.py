from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///book_wishlist.db', echo=True)

class Book(Base):

    ''' Represents one book in a user's list of books'''

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    read = Column(Boolean, default=False)


    def __str__(self):
        read_str = 'no'
        if self.read:
            read_str = 'yes'

        id_str = self.id
        if id == -1:
            id_str = '(no id)'

        template = 'id: {} Title: {} Author: {} Read: {}'
        return template.format(id_str, self.title, self.author, read_str)


print('hello!!')

Base.metadata.create_all(engine)
