from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    schema = "books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books"
        results = connectToMySQL(cls.schema).query_db(query)
        books = []
        for row in results:
            books.append(cls(row))
        return books

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        results = connectToMySQL(cls.schema). query_db(query, data)
        return results

    @classmethod
    def get_from_author(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors on favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL(cls.schema). query_db(query, data)
        book = cls( results[0] )
        for row in results:
            author_data = {
                'id': row['authors.id'],
                'name': row['name'],
                "created_at": row['authors.created_at'],
                "updated_at": row['authors.updated_at']
            }
            book.authors.append( author.Author( author_data ) )
        return book

    @classmethod
    def new_favorite_books(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s)"
        results = connectToMySQL(cls.schema). query_db(query, data)
        books = []
        for row in results:
            books.append(cls(row))
        return books

    