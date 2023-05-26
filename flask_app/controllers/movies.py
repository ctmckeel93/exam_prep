from flask_app import app
from flask import render_template, session, url_for, redirect, request, flash
from flask_app.models import movie

@app.route("/movies/create")
def add_movie():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    return render_template("add_movie.html")

@app.route("/movies/process", methods=["POST"])
def create_movie():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    if not movie.Movie.is_valid(request.form):
        return redirect(url_for("add_movie"))
    else:
        data = {
            "title": request.form["title"],
            "genre": request.form["genre"],
            "release_year": request.form["release_year"],
            "description": request.form["description"],
            "user_id": int(request.form["user_id"])
        }
        movie.Movie.create(data)
        return redirect("/dashboard")

@app.route("/movies/edit/<int:id>")
def edit_movie(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    one_movie = movie.Movie.get_one_with_user({"id": id})
    return render_template("edit_movie.html", one_movie = one_movie)

@app.route("/movies/update/<int:id>", methods=["POST"])
def update_movie(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    if not movie.Movie.is_valid(request.form):
        return redirect(url_for("edit_movie"))
    else:
        data = {
            "id": id,
            "title": request.form["title"],
            "genre": request.form["genre"],
            "release_year": request.form["release_year"],
            "description": request.form["description"],
            "user_id": int(session["logged_in"])
        }
        movie.Movie.update(data)
        return redirect("/dashboard")
    
@app.route("/movies/<int:id>")
def one_movie(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    user_id = int(session["logged_in"])
    movie_from_db = movie.Movie.get_one_with_user({"id": id})
    return render_template("one_movie.html", one_movie = movie_from_db, user_id = user_id)

@app.route("/movies/delete/<int:id>")
def delete_movie(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    movie.Movie.destroy({"id":id})
    return redirect(url_for("dashboard"))