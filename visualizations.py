import populate_db

def visualize_data(df):
    print(df)
    # Check if the DataFrame is empty
    if df.empty:
        print("DataFrame is empty. Cannot visualize data.")
        return
        
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
    plt.xlabel('Title')
    plt.ylabel('Average Rating')
    plt.show()

    # Create scatter plot for IMDb and TMDb ratings correlation
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='IMDb Rating', y='TMDb Rating', data=df)
    plt.title('IMDb vs TMDb Ratings Correlation')
    plt.xlabel('IMDb Rating')
    plt.ylabel('TMDb Rating')
    plt.show()

    # Create pie chart for genre distribution
    plt.figure(figsize=(10, 6))
    genre_counts = df['Genre'].value_counts()
    if not genre_counts.empty:
        genre_counts.plot.pie(autopct='%1.1f%%')
        plt.title('Genre Distribution of Recommended Movies')
        plt.show()
    else:
        print("Genre data is empty. Cannot create pie chart.")