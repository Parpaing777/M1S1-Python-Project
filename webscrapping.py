"""
Web Scraping TMDB with tmdbsimple
"""
import tmdbsimple as tmdb
import pickle
from tqdm import tqdm

# Set the API key
tmdb.API_KEY = 'SECRET KEY' # REMEMBER TO CHANGE THIS WHEN YOU PUSH TO GITHUB

# List to store raw data
raw_docs = []

# Since the API only gets 20 movies per page, we need to loop through the pages
nbMovies = 300 # Number of movies to fetch 
nbPerPage = 20 # Number of movies per page (fixed by the API)
pages = (nbMovies // nbPerPage) + (1 if nbMovies % nbPerPage > 0 else 0) # Add 1 if there is a remainder

# Loop through the trending page
# trending = tmdb.Trending(media_type='movie', time_window='week') # Weekly trending movies

# Loop through top rated page
top_rated = tmdb.Movies() # Top rated movies

for page in tqdm(range(1, pages +1)):
    # response = trending.info(page=page)
    response = top_rated.top_rated(page=page)
    for movie in response['results']:
        if len(raw_docs) < nbMovies: # If the number of movies needed is not yet reached
            # Now extract the details for the movie
            metadata = {
                'title': movie.get('title', 'Unknown'), # Movie title (default to 'Unknown' if not found)
                'Director': 'Unknown', # Placeholder
                'rating': movie.get('vote_average', 'N/A'), # Movie rating (default to 'N/A' if not found). Float number
                'Synopsis': movie.get('overview', 'No Synopsis'),
                'release_date': movie.get('release_date', 'Unknown'), # String
                'runtime': None # Placeholder for now. Have to get this from another API call
            }

            # Runtime fetch (since it's not in the trending API)
            movie_info = tmdb.Movies(movie['id']).info()
            metadata['runtime'] = movie_info.get('runtime', 'N/A')

            # Credits fetch (to get the director)
            credits = tmdb.Movies(movie['id']).credits()
            for crew in credits['crew']:
                if crew['job'] == 'Director':
                    metadata['Director'] = crew['name']
                    break

            # Append the metadata to the raw_docs list
            raw_docs.append(metadata)


# Save the raw data to a pickle file for later use
with open('raw_docs_300.pkl', 'wb') as f:
    pickle.dump(raw_docs, f)