import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3 
import sys
def calc_avg_rating(cur, file):
    genre_list = [g[0] for g in cur.execute('SELECT DISTINCT genre FROM imdb_genres').fetchall()]
    while True: 
        print("Genre List: ", end = "")
        print(genre_list)
        genre = input("Enter a Genre From the List: ")
        if genre in genre_list:
            break
        print("Genre Not Found")
    movie_list = [g[0] for g in cur.execute('SELECT title FROM imdb_info JOIN imdb_genres ON imdb_info.genre_id = imdb_genres.genre_id WHERE genre = ?', (genre,)).fetchall()]
    while True: 
        print("Movie List: ", end = "")
        print(movie_list)
        movie = input("Enter a Movie From the List: ")
        if movie in movie_list:
            break
        print("Movie Not Found")
    imdb_rating, tmdb_rating = cur.execute('SELECT imdb_rating,tmdb_rating FROM imdb_info JOIN tmdb_info ON imdb_info.id = tmdb_info.id WHERE imdb_info.title = ?', (movie,)).fetchone()
    if tmdb_rating is None:
        tmdb_rating = imdb_rating 
    avg_rating = (imdb_rating + tmdb_rating)/2
    print("Average Rating: " , avg_rating)
    print("Movie Title:" , movie, file = file, end = '  ')
    print("Average Rating:" , avg_rating, file = file)
    print(file=file)


def calc_avg_genre_rating(cur, file):
    print("Average Ratings for Movies in Each Genre: ", file=file)
    for imdb_rating, tmdb_rating, genre in cur.execute("""
    SELECT avg(imdb_rating),avg(tmdb_rating),genre FROM imdb_info 
    JOIN tmdb_info ON imdb_info.id = tmdb_info.id, 
    imdb_genres ON imdb_info.genre_id = imdb_genres.genre_id GROUP BY genre
    """):
        if tmdb_rating is None:
            tmdb_rating = imdb_rating
        avg_genre_rating = (imdb_rating + tmdb_rating)/2
        print(genre, file = file, end = ' ')
        print("Average Rating: " , avg_genre_rating, file = file)
    print(file=file)

def count_genres(cur, file):
    genre_counts = {}

    for row in cur.execute("""
        SELECT genre FROM imdb_info 
        JOIN imdb_genres ON 
        imdb_info.genre_id = imdb_genres.genre_id
    """):
        genre = row[0]
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Print the genre counts
    print("Number of Movies in Each Genre: ", file=file)
    for genre, count in genre_counts.items():
        print(f"Number of Movies in '{genre}': {count}", file=file)
    print(file=file)

def calc_top10_avg(cur,file):
    print("Average of TMBd and IMBd Ratings for the Top 10 Movies", file=file)
    movie_ratings = []
    for row in cur.execute("""
        SELECT imdb_info.id, imdb_rating, tmdb_rating, imdb_info.title 
                           
        FROM imdb_info 
        JOIN tmdb_info ON imdb_info.id = tmdb_info.id 
        """):
        movie_id, imdb_rating, tmdb_rating, title = row
        if tmdb_rating is None:
            tmdb_rating = imdb_rating
        avg_movie_rating = (imdb_rating + tmdb_rating) / 2
        movie_ratings.append((title, avg_movie_rating))

    # Sort the movie_ratings list by average rating in descending order
    movie_ratings.sort(key=lambda x: x[1], reverse=True)

    # Extract top movies and their ratings
    top_movies = [movie for movie, _ in movie_ratings[:10]]
    top_ratings = [rating for _, rating in movie_ratings[:10]]
    for movie, rating in zip(top_movies, top_ratings):
        print(f"'{movie}': {rating}", file=file)


def main():
    con = sqlite3.connect('movie_data.db')
    cur = con.cursor()
    with open('calculations.txt', 'w') as file:
        calc_avg_rating(cur, file)
        calc_avg_genre_rating(cur,file)
        count_genres(cur,file)
        calc_top10_avg(cur,file)
    



if __name__ == "__main__":
    main()