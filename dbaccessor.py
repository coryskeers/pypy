import sqlite3
import re

class DBAccessor:

    def __init__(self):
        self.connect()
        self.phonemes = ['AA', 'AE', 'AH', 'AO', 'AW',
                         'AY', 'EH', 'ER', 'EY', 'IH',
                         'IY', 'OW', 'OY', 'UH', 'UW',
                         'B', 'D', 'G', 'K', 'P', 'T',
                         'W', 'Y', 'M', 'N', 'NG', 'L',
                         'R', 'DH', 'F', 'S', 'SH', 'TH',
                         'V', 'Z', 'ZH', 'HH', 'CH', 'JH']
        
    def connect(self, dbName = 'dictionary'):
        self.dbName = dbName
        self.conn = sqlite3.connect(dbName + '.db')
        self.cur = self.conn.cursor()
        print('Connected to: {0}'.format(dbname)

    def getInfo(self, word):
    '''Return all the information of a given word. Returns a single element list
    as [(word, pronunciation, syllables, vector, part, def)]'''
        try:
            self.cur.execute("SELECT * FROM dictionary WHERE word = ?", (word,))
            return self.cur.fetchall() #returns a list of tuples, where items
            #in the tuple are each of the elements from the database,
            #given as [(word, pronunciation, syllables, vector, part, def)]
        except:
            return -1

    def vec2phonemes(self, vector):
    '''Takes a vector and returns a list of individual phonemes after translation.'''
        translated = []
        i = 0
        try:
            while vector > 0:
                if vector % 2 == 1:
                    translator.append(self.phonemes[i])
                    vector -= 1
                vector /= 2
                i += 1
        except:
            return translated

    def phonemes2vec(self, p):
    '''Takes p list of preprocessed phonemes or a long string of unprocessed
    and returns the translated vector.'''
        try:
            if isinstance(p, list):
                return sum([2**self.phonemes.index(c) for c in p])
            else:
                return sum([2**self.phonemes.index(c.strip(string.digits)) for c in p.split()])
        except:
            return -1
