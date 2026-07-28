import requests

API_KEY = "acfdee38"

def get_movie_details(title):
    url = "https://www.omdbapi.com/"

    params = {
        "apikey": API_KEY,
        "t": title
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return {
            "poster": data.get("Poster"),
            "plot": data.get("Plot"),
            "actors": data.get("Actors"),
            "runtime": data.get("Runtime"),
            "language": data.get("Language"),
            "awards": data.get("Awards"),
            "imdbRating": data.get("imdbRating"),
            "genre": data.get("Genre"),
            "year": data.get("Year")
        }

    return None