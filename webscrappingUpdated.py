"""
Web Scraping TMDB with tmdbsimple
"""
import tmdbsimple as tmdb
import pickle
from tqdm import tqdm

# Set the API key
tmdb.API_KEY = 'API Secret' # REMEMBER TO CHANGE THIS WHEN YOU PUSH TO GITHUB

# List to store raw data
raw_docs = []

# Since the API only gets 20 movies per page, we need to loop through the pages
nbMovies = 5 # Number of movies to fetch 
nbTV = 5 # Number of TV shows to fetch


# Helper function to get the metadata for movies and TV shows
def get_metadata(item, media_type):
    """
    Fetch metadata for Movies or TV series
    """
    metadata = {
        'media_type': media_type,
        'title': item.get('title') or item.get('name', 'Unknown'), # Movie title (default to 'Unknown' if not found)
        'Director': None, # Placeholder, (Only for movies)
        'Created By': None, # Placeholder, (Only for TV shows)
        'rating': item.get('vote_average', 'N/A'), # Movie rating (default to 'N/A' if not found). Float number
        'Synopsis': item.get('overview', 'No Synopsis'),
        'release_date': item.get('release_date') or item.get('first_air_date', 'Unknown'), # String
        'runtime': None, # Placeholder for now. Have to get this from another API call
        'Num seasons': None, # Placeholder for TV shows
        'Num episodes': None, # Placeholder for TV shows
        'Status': None # Placeholder for TV shows (e.g. 'Ended', 'Returning Series')
    }

    # Fetching additional metadata based on the media type
    if media_type == 'movie': # For movies
        details = tmdb.Movies(item['id']).info()
        metadata['runtime'] = details.get('runtime', 'N/A') # Runtime in minutes

        # Credits fetch (to get the director)
        credits = tmdb.Movies(item['id']).credits()
        for crew in credits['crew']:
            if crew['job'] == 'Director':
                metadata['Director'] = crew['name']
                break

    elif media_type == 'tv': # For TV shows
        details = tmdb.TV(item['id']).info()
        # The episode runtime could be empty sometimes, due to incomplete DB
        metadata['runtime'] = (
            details.get('episode_run_time', ['N/A'])[0] if details.get('episode_run_time') else 'N/A'
        )
        metadata['Num seasons'] = details.get('number_of_seasons', 'N/A')
        metadata['Num episodes'] = details.get('number_of_episodes', 'N/A')
        metadata['Status'] = details.get('status', 'Unknown')
        
        # Fetch the creator
        if 'created_by' in details: # TV shows could have multiple creators
            creators = [creator['name'] for creator in details['created_by']] # List of creators
            metadata['Created By'] = ', '.join(creators) if creators else 'Unknown'
        
    return metadata

# Scraping data
def scrape_tmdb(media_type, nbItems):
    """
    Scraper function to fetch data from TMDB
    """
    items = [] # List to store the items
    nbPerPage = 20 # Number of movies per page (fixed by the API)
    pages = (nbItems // nbPerPage) + (1 if nbItems % nbPerPage > 0 else 0) # Add 1 if there is a remainder

    fetcher = tmdb.Movies() if media_type == 'movie' else tmdb.TV() # Fetcher object based on media type
    endpoint = fetcher.top_rated

    for page in tqdm(range(1, pages +1), desc=f'Fetching {media_type}s'):
        response = endpoint(page=page)
        for item in response['results']:
            if len(items) < nbItems:
                metadata = get_metadata(item, media_type)
                items.append(metadata)

    return items

# Fetching movies
raw_movies = scrape_tmdb('movie', nbMovies)
raw_TV = scrape_tmdb('tv', nbTV)

raw_docs = raw_movies + raw_TV

# Save the raw data to a pickle file for later use
with open('raw_MVTV_300.pkl', 'wb') as f:
    pickle.dump(raw_docs, f)

