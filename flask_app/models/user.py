from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import movie
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "exam_prep"
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.movies = []
        
        
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if results:
            user_from_db = results[0]
            return cls(user_from_db)
        else:
            return False
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if results:
            user_from_db = results[0]
            return cls(user_from_db)
        else:
            return False
        
    
    @staticmethod
    def is_valid(user_dict):
        is_valid = True
        
        if len(user_dict["username"]) < 2:
            is_valid = False
            flash("username should have at least 2 characters")
        if len(user_dict["email"]) < 2:
            is_valid = False
            flash("Email should have at least 2 characters")
        if not EMAIL_REGEX.match(user_dict['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user_dict["password"]) < 2:
            is_valid = False
            flash("First name should have at least 2 characters")
        if user_dict["password_confirmation"] != user_dict["password"] :
            is_valid = False
            flash("Password must match password confirmation")
        return is_valid
    
    @classmethod
    def get_user_with_movies(cls, data):
        
        query = "SELECT * FROM users LEFT JOIN movies ON users.id = movies.user_id WHERE id=%(id)s;"
        
        results = connectToMySQL(cls.db).query_db(query, data)
        
        user = cls(results[0])
        
        for row in results:
            
            movie_data = {
                "id": row["movies.id"],
                "title": row["title"],
                "genre": row["genre"],
                "release_year": row["release_year"],
                "description": row["description"],
                "user_id": row["user_id"]
            }
            
            user.movies.append(movie.Movie(movie_data))
            
        return user
            
        
    
        
        
    