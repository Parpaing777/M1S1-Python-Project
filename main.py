import pickle
with open('raw_docs_300.pkl', 'rb') as f:
    raw_docs = pickle.load(f)

# print(raw_docs)

from MovieClasses import MvDoc, Director
import datetime

collection = []
for doc in raw_docs:
    title = doc['title']
    director = doc['Director']
    rating = f'{doc["rating"]:.2f} out of 10' # cut the rating to 2 decimal places
    synopsis = doc['Synopsis']
    release_date = datetime.datetime.strptime(doc['release_date'], '%Y-%m-%d').strftime('%B %d, %Y') # format the date to real date time format
    runtime = f'{doc["runtime"]//60}h {doc["runtime"]%60}m' #convert runtime to hours and minutes

    mv = MvDoc(title,director,rating, synopsis, release_date, runtime)
    collection.append(mv)

# print(collection)


id2mv = {} # Dictionary to store movies with their IDs ( Key: ID, Value: Movie title)
for i, movie in enumerate(collection):
    id2mv[i] = movie.title

id2dir = {} # Dict to group movies by Directors (Key: Director name, Value: Director object)
for i, movie in enumerate (collection):
    if movie.director not in id2dir:
        id2dir[movie.director] = Director(movie.director)
    id2dir[movie.director].add(id2mv[i])

# print(id2dir)

from Corpus import MvCorpus as mc

corpus = mc('Top 300 Movies')
for movie in collection:
    corpus.add(movie)

# corpus.show(20, 'title') 
# print(corpus)
corpus.PKLsave('Corpus_Top300')
# corpus.PDsave('Corpus_Top300')