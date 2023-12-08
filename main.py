import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3 

# Constants
IMDB_API_KEY = "cbfa71b7"
TMDB_API_KEY = "5d26fbe8ace3af695a9550c71fbd13c4"
IMDB_BASE_URL = "http://www.omdbapi.com/?i=tt3896198&apikey=cbfa71b7"
TMDB_BASE_URL = "https://api.themoviedb.org/3/"

# Function to fetch data from IMDb API
def fetch_imdb_data(title):
    params = {'apikey': IMDB_API_KEY, 't': title}
    response = requests.get(IMDB_BASE_URL, params=params)
    data = response.json()
    return data

# Function to fetch data from TMDb API
def fetch_tmdb_data(title):
    params = {'api_key': TMDB_API_KEY, 'query': title}
    response = requests.get(TMDB_BASE_URL + 'search/movie', params=params)
    data = response.json()
    return data

# Function to calculate average rating
def calculate_average_rating(imdb_rating, tmdb_rating):
    return (imdb_rating + tmdb_rating) / 2

# Function to visualize data
# Function to visualize data
def visualize_data(df):
    # Check if the DataFrame is empty
    if df.empty:
        print("DataFrame is empty. Cannot visualize data.")
        return

    # Check if 'Average Rating' column exists in the DataFrame
    if 'Average Rating' not in df.columns:
        print("No 'Average Rating' column found. Cannot visualize data.")
        return

# Function to visualize data
def visualize_data(df):
    # Check if the DataFrame is empty
    if df.empty:
        print("DataFrame is empty. Cannot visualize data.")
        return

    # Check if 'Title' column exists in the DataFrame
    if 'Title' not in df.columns:
        print("No 'Title' column found. Cannot visualize data.")
        return

    # Check if 'Average Rating' column exists in the DataFrame
    if 'Average Rating' not in df.columns:
        print("No 'Average Rating' column found. Cannot visualize data.")
        return

    # Check if there are non-empty and non-NaN values in 'Average Rating' column
    valid_ratings = df['Average Rating'].dropna()
    if valid_ratings.empty:
        print("No valid 'Average Rating' values found. Cannot visualize data.")
        return

    # Create bar chart for average ratings with a default color
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    df.plot(kind='bar', x='Title', y='Average Rating', color='skyblue', legend=False)
    plt.title('Average Ratings of Movies')
    plt.show()

    # Create scatter plot for IMDb and TMDb ratings correlation
    sns.scatterplot(x='IMDb Rating', y='TMDb Rating', data=df)
    plt.title('IMDb vs TMDb Ratings Correlation')
    plt.show()

    # Create pie chart for genre distribution
    genre_counts = df['Genre'].value_counts()
    if not genre_counts.empty:
        genre_counts.plot.pie(autopct='%1.1f%%')
        plt.title('Genre Distribution of Recommended Movies')
        plt.show()
    else:
        print("Genre data is empty. Cannot create pie chart.")


# Main function
def main():
    # Example movie title
    movie_title = "Inception"

    # Fetch data from IMDb
    imdb_data = fetch_imdb_data(movie_title)
    imdb_title = imdb_data.get('Title')
    imdb_year = imdb_data.get('Year')
    imdb_genre = imdb_data.get('Genre')
    imdb_rating = float(imdb_data.get('imdbRating', 0))

    # Fetch data from TMDb
    tmdb_data = fetch_tmdb_data(movie_title)
    # Fix for potential missing results
    tmdb_title = tmdb_data.get('results', [{}])[0].get('original_title', '')
    tmdb_cast = tmdb_data.get('results', [{}])[0].get('cast', [])
    tmdb_rating = tmdb_data.get('results', [{}])[0].get('vote_average', 0)

    # Calculate average rating
    avg_rating = calculate_average_rating(imdb_rating, tmdb_rating)

    # Create DataFrame
    data = {'Title': [imdb_title],
            'Year': [imdb_year],
            'Genre': [imdb_genre],
            'IMDb Rating': [imdb_rating],
            'TMDb Rating': [tmdb_rating],
            'Average Rating': [avg_rating]}

    df = pd.DataFrame(data)

    # Visualize data
    visualize_data(df)

if __name__ == "__main__":
    main()
