import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Constants
IMDB_API_KEY = "cbfa71b7"
TMDB_API_KEY = "5d26fbe8ace3af695a9550c71fbd13c4"
IMDB_BASE_URL = "ttp://www.omdbapi.com/?i=tt3896198&apikey=cbfa71b7"
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
def visualize_data(df):
    # Create bar chart for average ratings
    sns.barplot(x='Title', y='Average Rating', data=df)
    plt.title('Average Ratings of Movies')
    plt.show()

    # Create scatter plot for IMDb and TMDb ratings correlation
    sns.scatterplot(x='IMDb Rating', y='TMDb Rating', data=df)
    plt.title('IMDb vs TMDb Ratings Correlation')
    plt.show()

    # Create pie chart for genre distribution
    genre_counts = df['Genre'].value_counts()
    genre_counts.plot.pie(autopct='%1.1f%%')
    plt.title('Genre Distribution of Recommended Movies')
    plt.show()

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
    tmdb_title = tmdb_data['results'][0]['original_title']
    tmdb_cast = tmdb_data['results'][0]['cast']
    tmdb_rating = tmdb_data['results'][0]['vote_average']

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

