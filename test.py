from Corpus import MdCorpus as mdc

corpus = mdc('test').PKLload('300MVTV')

# print(corpus.concorde('Tarantino'))
# corpus.vocabularize()
corpus.stats()