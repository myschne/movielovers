import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3 
import sys



# Constants
IMDB_API_KEY = "cbfa71b7"
TMDB_API_KEY = "5d26fbe8ace3af695a9550c71fbd13c4"
IMDB_BASE_URL = "https://www.omdbapi.com/" 
TMDB_BASE_URL = "https://api.themoviedb.org/3/movie/"


# Function to fetch data from IMDb API
def fetch_imdb_data(title):
    params = {'apikey': IMDB_API_KEY, 't': title}
    # params = {'t': title}
    
    response = requests.get(IMDB_BASE_URL, params=params)
    data = response.json()
    return data

def search_imdb_data(search):
    params = {'apikey': IMDB_API_KEY, 's': search}
    # params = {'t': title}
    
    response = requests.get(IMDB_BASE_URL, params=params)
    data = response.json()
    return data

# Function to fetch data from TMDb API
def fetch_tmdb_data(title):
    params = {'api_key': TMDB_API_KEY, 'query': title}
    response = requests.get(TMDB_BASE_URL + title, params=params)
    data = response.json()
    print(data,"tmdb")
    return data

# Function to calculate average rating
def calculate_average_rating(imdb_rating, tmdb_rating):
    return (imdb_rating + tmdb_rating) / 2



   



# Main function
def main():
    
    #Get Data from IMDB API
    con = sqlite3.connect('movie_data.db')
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS imdb_info( "
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title VARCHAR[64] NOT NULL, "
            "year INTEGER NOT NULL, "
            "imdb_rating REAL NOT NULL)"
    )


    cur.execute(
        "CREATE TABLE IF NOT EXISTS imdb_genres("
            "id INTEGER PRIMARY KEY NOT NULL, "
            "genre VARCHAR[64] NOT NULL)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS tmdb_info("
            "id INTEGER PRIMARY KEY NOT NULL, "
            "title VARCHAR[64] NOT NULL, "
            "tmdb_rating REAL)"
    )
    con.commit()
    #Get User Input
    i = 0
    while i == 0: 
        search = input("Enter a search term: ")
        results = search_imdb_data(search)
        if results ['Response'] != 'True':
            print(results ['Error'])
            continue
    
    

        for movie in results['Search']:
            if i < 25:
                movie = fetch_imdb_data(movie['Title'])
                if(movie["Response"] == "False"):
                    break
                title = movie['Title']
                imdb_rating = movie['imdbRating']
                year = movie['Year']
                genre = movie['Genre'].split(',')[0]
                if imdb_rating == 'N/A':
                    break

                cur.execute(
                    "INSERT INTO imdb_info(title, year, imdb_rating) "
                    "VALUES(?, ?, ?)",
                    (title, year, float(imdb_rating))
                )
                cur.execute(
                    "SELECT last_insert_rowid()"
                )

                id = cur.fetchone()

                cur.execute(
                    "INSERT INTO imdb_genres(id, genre) "
                    "VALUES(?,?)",
                    (id[0],genre)
                )
                print(movie)

                #Fetch Data from TMDB
                
                imdb_id = movie["imdbID"]
                # tmdb_data = fetch_tmdb_data(genre_list[genre][i])
                tmdb_data = fetch_tmdb_data(imdb_id)


                tmdb_rating = None
                if("success" not in tmdb_data):
                    tmdb_rating = tmdb_data['vote_average']

                cur.execute(
                    "INSERT INTO tmdb_info(id, title, tmdb_rating) "
                    "VALUES(?, ?, ?)",
                    (id[0],title, tmdb_rating)
                )
                
                i += 1
                print(movie)

        if i == 0:
           print("No Movies Found")

    cur.execute(
        "SELECT * FROM imdb_info "
    )
    con.commit()
    con.close()



if __name__ == "__main__":
    main()