from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    schema = "books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors"
        results = connectToMySQL(cls.schema).query_db(query)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors

    @classmethod
    def save(cls, data):
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        results = connectToMySQL(cls.schema). query_db(query, data)
        return results

    @classmethod
    def favorite(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s)"
        return connectToMySQL(cls.schema).query_db(query, data)
    
    @classmethod
    def new_favorite_author(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s)"
        results = connectToMySQL(cls.schema).query_db(query, data)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors

    @classmethod
    def get_from_books(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s"
        results = connectToMySQL(cls.schema).query_db(query, data)
        author = cls( results[0] )
        for row_books in results:
            book_data = {
                "id": row_books['books.id'],
                "title": row_books['title'],
                "num_of_pages": row_books['num_of_pages'],
                "created_at": row_books['books.created_at'],
                "updated_at": row_books['books.updated_at']
            }
            author.books.append( book.Book( book_data) )
        return author