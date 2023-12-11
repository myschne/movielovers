import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3 
import sys
import imdb


# Constants
IMDB_API_KEY = "cbfa71b7"
TMDB_API_KEY = "5d26fbe8ace3af695a9550c71fbd13c4"
IMDB_BASE_URL = "https://www.omdbapi.com/" 
TMDB_BASE_URL = "https://api.themoviedb.org/3/movie/550"

#Genre Lists
action_movies = [
"Die Hard",
"Mad Max: Fury Road",
"The Dark Knight",
"Terminator 2: Judgment Day",
"John Wick",
"Gladiator",
"The Bourne Identity",
"Mission: Impossible - Fallout",
"Kill Bill: Volume 1",
"Lethal Weapon",
"The Matrix",
"Rambo: First Blood",
"The Raid: Redemption",
"Predator",
"Speed",
"Atomic Blonde",
"Taken",
"Die Hard with a Vengeance",
"Ip Man",
"Black Panther"
]
comedy_movies = [
"Anchorman: The Legend of Ron Burgundy",
"Superbad",
"The Hangover",
"Bridesmaids",
"Dumb and Dumber",
"Ferris Bueller's Day Off",
"The Grand Budapest Hotel",
"Shaun of the Dead",
"Airplane!",
"The Princess Bride",
"Ghostbusters",
"Caddyshack",
"Napoleon Dynamite",
"Groundhog Day",
"The 40-Year-Old Virgin",
"Dodgeball: A True Underdog Story",
"Zoolander",
"Mean Girls",
"Office Space",
"Pineapple Express"
]
drama_movies = [
"The Shawshank Redemption",
"The Godfather",
"Schindler's List",
"Forrest Gump",
"The Dark Knight",
"Gladiator",
"The Silence of the Lambs",
"Schindler's List",
"The Green Mile",
"A Beautiful Mind",
"The Pursuit of Happyness",
"The Social Network",
"The Revenant",
"12 Years a Slave",
"Atonement",
"Good Will Hunting",
"American Beauty",
"The Pianist",
"Casablanca",
"The Shape of Water"
]
romance_movies = [
"The Notebook",
"Titanic",
"Pride and Prejudice",
"Eternal Sunshine of the Spotless Mind",
"La La Land",
"Before Sunrise",
"The Fault in Our Stars",
"500 Days of Summer",
"Pretty Woman",
"The Princess Bride",
"Notting Hill",
"Casablanca",
"Romeo + Juliet",
"Brokeback Mountain",
"A Walk to Remember",
"When Harry Met Sally",
"Silver Linings Playbook",
"The Shape of Water",
"The Phantom of the Opera",
"Sense and Sensibility"
]
sci_fi_movies = [
"Blade Runner",
"The Matrix",
"Star Wars: Episode IV - A New Hope",
"Interstellar",
"2001: A Space Odyssey",
"The Terminator",
"E.T. the Extra-Terrestrial",
"Inception",
"The Fifth Element",
"Jurassic Park",
"The Day the Earth Stood Still",
"The War of the Worlds",
"Back to the Future",
"Avatar",
"The Martian",
"The Matrix Reloaded",
"Close Encounters of the Third Kind",
"The Empire Strikes Back",
"The Hitchhiker's Guide to the Galaxy",
"Ex Machina"
]
genre_list = {'Action': action_movies, 'Comedy': comedy_movies, 'Drama': drama_movies, 'Romance': romance_movies, 'Sci-Fi': sci_fi_movies}
    

# Function to fetch data from IMDb API
def fetch_imdb_data(title):
    params = {'apikey': IMDB_API_KEY, 't': title}
    # params = {'t': title}
    
    response = requests.get(IMDB_BASE_URL, params=params)
    data = response.json()
    return data

# Function to fetch data from TMDb API
def fetch_tmdb_data(title):
    params = {'api_key': TMDB_API_KEY, 'query': title}
    response = requests.get(TMDB_BASE_URL, params=params)
    data = response.json()
    print(data,"tmdb")
    return data

# Function to calculate average rating
def calculate_average_rating(imdb_rating, tmdb_rating):
    return (imdb_rating + tmdb_rating) / 2



   



# Main function
def main():
    

    #Get User Input for Genre
    while True: 
        print("Genre List: ", end = "")
        print(genre_list.keys())
        genre = input("Enter a Genre From the List: ")
        if genre in genre_list:
            break
        print("Genre Not Found")
    


    #Get Data from API

    con = sqlite3.connect('movie_data.db')
    cur = con.cursor()
    
    cur.execute(
        "CREATE TABLE IF NOT EXISTS imdb_info( "
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title VARCHAR[64] NOT NULL, "
            "year INTEGER NOT NULL, "
            "rating REAL NOT NULL)"
    )
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS imdb_genres("
            "id INTEGER PRIMARY KEY NOT NULL, "
            "genre VARCHAR[64] NOT NULL)"
    )
    con.commit()
    
    i = 0

    for movie in genre_list[genre]:
        if i < 20:
            movie = fetch_imdb_data(genre_list[genre][i])
            title = movie['Title']
            rating = movie['Ratings']['1']['Value']
            year = movie['Year']
            

            cur.execute(
                "INSERT INTO imdb_info(title, year, rating) "
                "VALUES(?, ?, ?)",
                (title, year, rating)
            )

            cur.execute(
                "SELECT last_insert_rowid()"
            )

            id = cur.fetchone()['last_insert_rowid()']

            cur.execute(
                "INSERT INTO imdb_genres(id, genre) "
                "VALUES(?,?)",
                (id,genre)
            )
            i += 1
            print(movie)
    cur.execute(
        "SELECT * FROM imdb_data "
    )


   

    # # Fetch data from TMDb
    # tmdb_data = fetch_tmdb_data(movie_title)
    
    # # Fix for potential missing results
    # tmdb_title = tmdb_data.get('original_title', '')
    # if not tmdb_title:
    #     #TODO
    #     x = 1
    # tmdb_cast = tmdb_data.get('cast', [])
    # tmdb_rating = tmdb_data.get('vote_average', 0)

    # # Calculate average rating
    # avg_rating = calculate_average_rating(imdb_rating, tmdb_rating)

    # # Create DataFrame
    # data = {'Title': [imdb_title],
    #         'Year': [imdb_year],
    #         'Genre': [imdb_genre],
    #         'IMDb Rating': [imdb_rating],
    #         'TMDb Rating': [tmdb_rating],
    #         'Average Rating': [avg_rating]}

    # df = pd.DataFrame(data)

    

if __name__ == "__main__":
    main()