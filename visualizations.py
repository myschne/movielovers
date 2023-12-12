import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3 
import sys

def visualize_data(cur):
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

    # Plotting the bar chart
    plt.bar(top_movies, top_ratings, color='skyblue')
    plt.xlabel('Movies')
    plt.ylabel('Average Rating')
    plt.title('Top Rated Movies Based on Average IMDb and TMDb Ratings')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Create scatter plot for IMDb and TMDb ratings correlation
    imdb_ratings = []
    tmdb_ratings = []

    for row in cur.execute("""
        SELECT imdb_rating, tmdb_rating 
        FROM imdb_info 
        JOIN tmdb_info ON imdb_info.id = tmdb_info.id 
        WHERE imdb_rating IS NOT NULL AND tmdb_rating IS NOT NULL
        """):
        imdb_rating, tmdb_rating = row
        imdb_ratings.append(imdb_rating)
        tmdb_ratings.append(tmdb_rating)

    # Plotting the scatter plot
    plt.scatter(imdb_ratings, tmdb_ratings, color='blue', alpha=0.5)
    plt.xlabel('IMDb Rating')
    plt.ylabel('TMDb Rating')
    plt.title('IMDb and TMDb Ratings Correlation')
    plt.grid(True)
    plt.show()

    
    # Create pie chart for genre distribution
    genre_counts = {}

    for row in cur.execute("""
        SELECT genre FROM imdb_info 
        JOIN imdb_genres ON 
        imdb_info.genre_id = imdb_genres.genre_id
    """):
        genre = row[0]
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Plotting the pie chart
    labels = genre_counts.keys()
    sizes = genre_counts.values()

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
    plt.title('Genre Distribution')
    plt.show()


def main():
    con = sqlite3.connect('movie_data.db')
    cur = con.cursor()
    visualize_data(cur)
if __name__ == "__main__":
    main()