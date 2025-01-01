"""
This script is used to load the raw scrapped data from the pickle file, create a collection of Movie and TV series and save it as a corpus.
"""
import pickle
with open('raw_MVTV_600.pkl', 'rb') as f:
    raw_docs = pickle.load(f)

# print(raw_docs)

from MovieClasses import MvDoc, Director, SeriDoc, Creator
import datetime

collection = []

for doc in raw_docs:
    if doc['media_type'] == 'movie':
        title = doc['title']
        director = doc['Director']
        rating = f'{doc["rating"]:.2f} out of 10' # cut the rating to 2 decimal places
        synopsis = doc['Synopsis']
        release_date = datetime.datetime.strptime(doc['release_date'], '%Y-%m-%d').strftime('%B %d, %Y') # format the date to real date time format
        runtime = f'{doc["runtime"]//60}h {doc["runtime"]%60}m' #convert runtime to hours and minutes (string)
        

        mv = MvDoc(title,director,rating, synopsis, release_date, runtime)
        collection.append(mv)

    elif doc['media_type'] == 'tv':
        title = doc['title']
        creator = doc['Created By']
        rating = f'{doc["rating"]:.2f} out of 10'
        synopsis = doc['Synopsis']
        release_date = datetime.datetime.strptime(doc['release_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        runtime = (f"{doc['runtime']} minutes per episode" if doc['runtime'] != 'N/A' else 'N/A')
        num_seasons = doc['Num seasons']
        num_episodes = doc['Num episodes']
        status = doc['Status']
        

        tv = SeriDoc(title, creator, rating, synopsis, release_date, runtime, num_seasons, num_episodes, status)
        collection.append(tv)

# print(collection)

id2media = {} # Dictionary to store movies/series with their IDs (Key: ID, Value: Movie/Series title)
for i, media in enumerate(collection):
    id2media[i] = media.title

id2dir = {} # Dict to group movies by Directors (Key: Director name, Value: Director object)
id2ctr = {} # Dict to group series by Creators (Key: Creator name, Value: Creator object)
for i, media in enumerate(collection):
    if hasattr(media,'director') and media.director is not None:
        if media.type == 'Movie':
            if media.director not in id2dir:
                id2dir[media.director] = Director(media.director)
            id2dir[media.director].add(id2media[i])
        
    if hasattr(media,'creator') and media.creator is not None:
        if media.type == 'TV Series':
            if media.creator != 'Unknown':
               creators = media.creator.split(', ')
            else:
                creators = [f'Unknown({id2media[i]})']
            for creator in creators:
                if creator not in id2ctr:
                    id2ctr[creator] = Creator(creator)
                id2ctr[creator].add(id2media[i])
            
    
# print(id2ctr)
# print(id2dir)


from Corpus import MdCorpus as mdc

corpus = mdc('600MvTv')
for media in collection:
    corpus.addMedia(media)

# corpus.show(20, 'title')
corpus.PKLsave('600MVTV')




