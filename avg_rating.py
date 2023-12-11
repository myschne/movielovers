import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3 
import sys

def main():
    con = sqlite3.connect('movie_data.db')
    cur = con.cursor()
    genre_list = [g[0] for g in cur.execute('SELECT DISTINCT genre FROM imdb_genres').fetchall()]
    while True: 
        print("Genre List: ", end = "")
        print(genre_list)
        genre = input("Enter a Genre From the List: ")
        if genre in genre_list:
            break
        print("Genre Not Found")
    movie_list = [g[0] for g in cur.execute('SELECT title FROM imdb_info JOIN imdb_genres ON imdb_info.id = imdb_genres.id WHERE genre = ?', (genre,)).fetchall()]
    while True: 
        print("Movie List: ", end = "")
        print(movie_list)
        movie = input("Enter a Movie From the List: ")
        if movie in movie_list:
            break
        print("Movie Not Found")

if __name__ == "__main__":
    main()