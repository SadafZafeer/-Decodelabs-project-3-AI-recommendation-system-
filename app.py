from flask import Flask, render_template, request, jsonify

from recommendation import recommend_movies, get_movie_titles
from utils.omdb import get_movie_details

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    movie = request.form["movie"]

    recommendations, matched_movie = recommend_movies(movie)

    final_movies = []

    for item in recommendations:

        details = get_movie_details(item["title"])

        if details:

            item.update(details)

        final_movies.append(item)

    return render_template(

        "result.html",

        movie=matched_movie,

        recommendations=final_movies

    )


@app.route("/autocomplete")
def autocomplete():

    q = request.args.get("q", "").lower()

    movies = get_movie_titles()

    result = [

        movie

        for movie in movies

        if q in movie.lower()

    ][:10]

    return jsonify(result)


if __name__ == "__main__":

    app.run(debug=True)