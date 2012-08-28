#!/usr/bin/env python
import json
from flask import Flask, render_template, request

from model import Book, Author, Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)


##################### BOOKS #################################
@app.route("/")
def main_page():
	s = Session()
	books = s.query(Book).all()
	authors = s.query(Author).all()
	s.close()

	return render_template('beta.html', books=books, authors=authors)


@app.route("/new_book")
def new_book():
	s = Session()
	authors = s.query(Author).all()
	s.close()

	return render_template('edit_book.html', other_authors=authors)


@app.route("/edit_book/<_id>")
def edit_book(_id):
	s = Session()
	b = s.query(Book).filter_by(id=_id).first()

	current_authors = b.authors
	authors = s.query(Author).all()

	other_authors = []
	for a in authors:
		if a not in b.authors:
			other_authors.append(a)
	s.close()

	return render_template('edit_book.html', book=b, other_authors=other_authors, current_authors=current_authors)

@app.route("/book_save")
def new_book_save():
	status, msg = True, ''

	b_name = request.args.get('name')

	s = Session()
	b = Book(b_name)

	for key, val in request.args.items():
		if key == 'name':
			continue
		a = s.query(Author).filter_by(id=key).first()
		b.authors.append(a)

	s.add(b)

	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The book with name %s already exists' % b_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})


@app.route("/book_save/<_id>")
def book_save(_id):
	status, msg = True, ''
	b_name = request.args.get('name')

	s = Session()
	b = s.query(Book).filter_by(id=_id).first()

	del b.authors[:]

	for key, val in request.args.items():
		if key == 'name':
			continue
		a = s.query(Author).filter_by(id=key).first()
		b.authors.append(a)

	b.name = b_name
	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The book with name %s already exists' % b_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})


@app.route("/remove_book")
def remove_book():
	b_id   = request.args.get('id')

	s = Session()
	b = s.query(Book).filter_by(id=b_id).first()

	s.delete(b)
	s.commit()
	s.close()

	return json.dumps({'ok': True, 'msg': ''})


@app.route("/search_book")
def search_book():
	return render_template('search_book.html')


@app.route("/search_book_go")
def search_book_go():
	b_pattern = request.args.get('book_pattern')
	a_pattern = request.args.get('author_pattern')

	s = Session()

	if not a_pattern:
		books = s.query(Book).filter(Book.name.like('%' + b_pattern + '%'))
	else:
		books = s.query(Book).filter(and_(Book.name.like('%' + b_pattern + '%'), \
		       Book.authors.any(Author.name.like('%' + a_pattern + '%'))))

	out = []
	for b in books:
		out.append({'id': b.id, 'name': b.name})

	s.close()

	return json.dumps(out)


##################### AUTHORS #################################
@app.route("/new_author")
def new_author():
	return render_template('edit_author.html')


@app.route("/edit_author/<_id>")
def edit_author(_id):
	s = Session()
	a = s.query(Author).filter_by(id=_id).first()
	s.close()

	return render_template('edit_author.html', author=a)


@app.route("/author_save")
def new_author_save():
	status, msg = True, ''

	a_name = request.args.get('name')

	s = Session()
	s.add(Author(a_name))

	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The author with name %s already exists' % a_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})


@app.route("/author_save/<_id>")
def author_save(_id):
	status, msg = True, ''

	a_name = request.args.get('name')

	s = Session()
	a = s.query(Author).filter_by(id=_id).first()

	a.name = a_name

	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The author with name %s already exists' % a_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})

@app.route("/remove_author")
def remove_author():
	a_id   = request.args.get('id')

	s = Session()
	a = s.query(Author).filter_by(id=a_id).first()

	s.delete(a)
	s.commit()

	s.close()

	return json.dumps({'ok': True, 'msg': ''})



