
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.author import Author
from flask import render_template, redirect, request, session


@app.route('/books')
def books():
    books = Book.get_all()
    return render_template("books.html", books = books)

@app.route('/book/create', methods = ['POST'])
def create_book():
    Book.save(request.form)
    return redirect('/books')

@app.route('/book/<int:id>')
def show_book(id):
    data = {
        "id":id
    }
    book_show = Book.get_from_author(data)
    fave_author = Author.new_favorite_author(data)
    return render_template("book_show.html", book = book_show, fave_author = fave_author)

@app.route('/fave/book', methods = ['POST'])
def fave_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.favorite(data)
    return redirect(f"/book/{request.form['book_id']}")