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

horror_movies = [
    "The Exorcist",
    "Psycho",
    "Get Out",
    "A Nightmare on Elm Street",
    "The Shining",
    "Halloween",
    "The Babadook",
    "The Conjuring",
    "Hereditary",
    "It Follows",
    "The Witch",
    "A Quiet Place",
    "Don't Breathe",
    "Paranormal Activity",
    "The Blair Witch Project",
    "Saw",
    "Cabin in the Woods",
    "The Sixth Sense",
    "The Ring",
    "Insidious"
]
war_movies = [
    "Saving Private Ryan",
    "Apocalypse Now",
    "Full Metal Jacket",
    "Dunkirk",
    "Platoon",
    "Hacksaw Ridge",
    "Black Hawk Down",
    "Letters from Iwo Jima",
    "The Thin Red Line",
    "1917"
]
documentary_movies = [
    "An Inconvenient Truth",
    "Man on Wire",
    "March of the Penguins",
    "Blackfish",
    "Won't You Be My Neighbor?",
    "Jiro Dreams of Sushi",
    "Amy",
    "The Act of Killing",
    "Icarus",
    "Free Solo"
]
thriller_movies = [
    "Se7en",
    "The Usual Suspects",
    "Memento",
    "Gone Girl",
    "Prisoners",
    "The Sixth Sense",
    "Zodiac",
    "Shutter Island",
    "Oldboy",
    "The Girl with the Dragon Tattoo"
]

genre_list = {'Action': action_movies, 'Comedy': comedy_movies, 'Drama': drama_movies, 
              'Romance': romance_movies, 'Sci-Fi': sci_fi_movies, 'Horror': horror_movies,
              'War': war_movies, 'Documentary':documentary_movies, 'Thriller': thriller_movies}
    

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
    response = requests.get(TMDB_BASE_URL + title, params=params)
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
            "tmdb_rating REAL NOT NULL)"
    )
    con.commit()
    
    i = 0

    for movie in genre_list[genre]:
        if i < 20:
            movie = fetch_imdb_data(genre_list[genre][i])
            if(movie["Response"] == "False"):
                i +=1
                break
            title = movie['Title']
            imdb_rating = movie['imdbRating']
            year = movie['Year']
            

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
            i += 1
            print(movie)

            #Fetch Data from TMDB
            
            imdb_id = movie["imdbID"]
            # tmdb_data = fetch_tmdb_data(genre_list[genre][i])
            tmdb_data = fetch_tmdb_data(imdb_id)


            tmdb_rating = -1
            if("success" not in tmdb_data):
                tmdb_rating = tmdb_data['vote_average']

            cur.execute(
                "INSERT INTO tmdb_info(id, title, tmdb_rating) "
                "VALUES(?, ?, ?)",
                (id[0],title, tmdb_rating)
            )
            
            i += 1
            print(movie)

    cur.execute(
        "SELECT * FROM imdb_info "
    )
    con.commit()
    con.close()


if __name__ == "__main__":
    main()