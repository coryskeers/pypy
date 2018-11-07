import sqlite3
import string
import csv
import re

class WordsDatabase:

    def __init__(self):
        self.connect()

    def connect(self, dbName = 'dictionary'):
        self.dbName = dbName
        self.conn = sqlite3.connect(dbName + '.db')
        self.cur = self.conn.cursor()
        print('Connected to: {0}'.format(dbName + '.db'))

    def close(self):
        self.conn.close()

    def dropTable(self):
        self.cur.execute('DROP TABLE {0}'.format(self.dbName))
        print("Table dropped.")

    def createTablesList(self):
        with open('cmu dict.txt') as infile:
            print('Beginning word load.')
            return [line.strip().split('  ',1) for line in infile if line[0] != ';']

    def createTable(self):
        self.cur.execute("CREATE TABLE dictionary (word TEXT, pronunciation TEXT, syllables INT, vector REAL, part TEXT, definition TEXT)")

    def loadTable(self):
        print('Building tables.')
        SQLtable = [(w, l[0], l[1], l[2])  for w, l in self.phonemeDict.items()]
        print('Executing SQL insertion.')
        self.cur.executemany("INSERT INTO dictionary (word, pronunciation, syllables, vector) VALUES (?, ?, ?, ?)", SQLtable)
        self.conn.commit()
        print('Done.')
        
    def createPhonemeDict(self):
        phonemes = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW', 'B', 'D', 'G', 'K', 'P', 'T', 'W', 'Y', 'M', 'N', 'NG', 'L', 'R', 'DH', 'F', 'S', 'SH', 'TH', 'V', 'Z', 'ZH', 'HH', 'CH', 'JH']
        def helper(p):
            return sum([2**phonemes.index(c.strip(string.digits)) for c in p.split()])
        L = self.createTablesList()
        self.phonemeDict = {i[0].lower():[i[1], len([c for c in i[1] if c in string.digits]), helper(i[1])] for i in L  }

    def pullDef(self, word):
        import requests
        from bs4 import BeautifulSoup
        baseurl = 'https://www.merriam-webster.com/dictionary/'
        fullurl = baseurl + word
        try:
            r = requests.get(fullurl)
            c = r.content
            soup = BeautifulSoup(c, 'lxml')
            sentencePart = soup.find(class_='important-blue-link').getText()
            definition = soup.find(id='dictionary-entry-1').getText().split(': ', 1)[1]
            definition = re.sub(r'\s\s+', ' ', definition)
            return (sentencePart, definition)
        except:
            return ('.', '.')

    def buildDefs(self):
        self.cur.execute("SELECT word, part, definition FROM dictionary WHERE part IS NULL LIMIT 30")
        l = self.cur.fetchall()
        lappend = []
        for tup in l:
            partDef = self.pullDef(tup[0])
            lappend.append((partDef[0], partDef[1], tup[0]))
        self.cur.executemany("UPDATE dictionary SET part=?, definition=? WHERE word=?", lappend)
        self.conn.commit()
        print("Completed up to {0}".format(lappend[-1][2]))
