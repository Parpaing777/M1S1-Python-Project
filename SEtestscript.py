"""
This script is for testing the functionalities of the search engine
"""
from Corpus import MdCorpus as mdc

corpus = mdc('test').PKLload('600MVTV')

# print(corpus.concorde('Tarantino'))
# corpus.vocabularize()
# print(corpus.Search('Vampire'))

from searchEngine import SearchEngine as se

search = se(corpus)

print(search.search('Tarantino'))