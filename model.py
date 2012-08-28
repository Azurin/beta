#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

import config


db = create_engine(config.app.db.url, echo_pool=True)

Session = sessionmaker(bind=db)
Base = declarative_base()


books_authors = Table(
	'books_authors', Base.metadata,
	Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
	Column('authors_id', Integer, ForeignKey('authors.id'), primary_key=True)
	)


class Book(Base):
	__tablename__ = 'books'

	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)

	authors = relation('Author', secondary=books_authors, backref='wrote')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Book('%s')>" % (self.name)


class Author(Base):
	__tablename__ = 'authors'

	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Author('%s')>" % (self.name)


def createDB():
	'''Create DB if it doesn't exist'''
	if db.has_table('books'):
		return

	Base.metadata.create_all(db)
	s = Session()

	a = Author('Mark Twain')
	b = Book('Tom Sawyer')
	b.authors.append(a)
	s.add(b)

	a = Author('Herbert Wells')
	gogol = Author('Nicolay Gogol')
	b = Book('Time Machine')
	b.authors.append(a)
	b.authors.append(gogol)
	s.add(b)

	b = Book('Taras Bulba')
	b.authors.append(gogol)
	s.add(b)
	
	s.commit()
	s.close()

