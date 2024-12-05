"""
Web Scraping TMDB with tmdbsimple
"""

import tmdbsimple as tmdb

# Set the API key
tmdb.API_KEY = '' # REMEMBER TO CHANGE THIS WHEN YOU PUSH TO GITHUB

# List to store raw data
raw_docs = []

# Since the API only gets 20 movies per page, we need to loop through the pages
nbMovies = 100
nbPerPage = 20
pages = (nbMovies // nbPerPage) + (1 if nbMovies % nbPerPage > 0 else 0) # Add 1 if there is a remainder

# Loop through the trending page
trending = tmdb.Trending(media_type='movie', time_window='week') # Weekly trending movies
for page in range(1, pages +1):
    response = trending.info(page=page)
    for movie in response['results']:
        if len(raw_docs) < nbMovies: # If the number of movies needed is not yet reached
            # Now extract the details for the movie
            metadata = {
                'title': movie.get('title', 'Unknown'), # Movie title (default to 'Unknown' if not found)
                'rating': movie.get('vote_average', 'N/A'), # Movie rating (default to 'N/A' if not found)
                'Synopsis': movie.get('overview', 'No Synopsis'),
                'release_date': movie.get('release_date', 'Unknown'), 
                'runtime': None # Placeholder for now. Have to get this from another API call
            }

            # Runtime fetch (since it's not in the trending API)
            movie_info = tmdb.Movies(movie['id']).info()
            metadata['runtime'] = movie_info.get('runtime', 'N/A')

            # Append the metadata to the raw_docs list
            raw_docs.append(metadata)


# Print the raw data
print(f'Fetched {len(raw_docs)} movies:')
for doc in raw_docs:
    print(doc)