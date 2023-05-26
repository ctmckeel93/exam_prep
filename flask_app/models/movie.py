from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
# from flask_app.models.user import User

class Movie:
    db = "exam_prep"
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.genre = data["genre"]
        self.year = data["release_year"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.creator = None
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movies;"
        results = connectToMySQL(cls.db).query_db(query)
        all_movies = []
        
        for row in results:
            all_movies.append(cls(row))
        return all_movies
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO movies (title, genre, release_year, description, user_id) VALUES (%(title)s,%(genre)s,%(release_year)s,%(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    
    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM movies LEFT JOIN users on users.id = movies.user_id WHERE movies.id=%(id)s;"
        
        results = connectToMySQL(cls.db).query_db(query, data)
        row = results[0]
        one_movie = cls(row)
        user_data = {
            "id": row["users.id"],
            "username": row["username"],
            "email": row["email"],
            "password": row["password"],
            "created_at": row["users.created_at"],
            "updated_at": row["users.updated_at"]
        }
        
        one_movie.creator = user.User(user_data)
        
        return one_movie
    
    @classmethod
    def update(cls, data):
        
        query = "Update movies SET title=%(title)s, genre=%(genre)s, release_year=%(release_year)s, description=%(description)s WHERE id = %(id)s;"

        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM movies WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def is_valid(movie):
        is_valid = True
        
        if len(movie["title"]) < 3:
            flash("Movie title must be at least 3 characters")
            is_valid = False
        if len(movie["genre"]) < 3:
            flash("Movie genre must be at least 3 characters")
            is_valid = False
        if len(movie["description"]) < 10:
            flash("Movie description must be at least 3 characters")
            is_valid = False
        return is_valid
            
    
    