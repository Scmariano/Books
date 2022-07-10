
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book
from flask import render_template, redirect, request, session

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def authors():
    authors = Author.get_all()
    return render_template("author.html", authors = authors)

@app.route('/author/create', methods = ['POST'])
def create_author():
    Author.save(request.form)
    return redirect('/authors')

@app.route('/author/<int:id>')
def author_show(id):
    data = {
        'id': id
    }
    author = Author.get_from_books(data)
    new_favorite = Book.new_favorite_books(data)

    return render_template("authors_show.html", author = author , new_favorite = new_favorite) 

@app.route('/new/favorite', methods = ['POST'])
def new_favorite():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.favorite(data)
    return redirect(f"/author/{request.form['author_id']}")