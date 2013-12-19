import json


class Base(object):
    @property
    def __self__(self):
        return self.__dict__

    def __json__(self):
        return json.dumps(self.__self__)


class File(Base):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        f = open(self.filename, 'r')
        content = f.read()

        content = content.replace('\n', '')
        content = content.replace('\r', '')

        for seperator in ['?', '!', ':']:
            content = content.replace(seperator, '.')

        separator = '.'

        self.sentences = [Sentence(s.strip(), separator) for s in content.split(separator) if s]

    def save(self):
        f = open(self.filename, 'w')

        json = self.__json__()

        f.write(json)
        f.close()

    @property
    def __self__(self):
        return {
            'sentences': [sentence.__self__ for sentence in self.sentences]
        }

    def __repr__(self):
        return ' '.join([sentence.__repr__() for sentence in self.sentences])


class Sentence(Base):
    def __init__(self, content, end):
        content = content.replace(',', ' ')
        self.words = [Word(w) for w in content.split(' ') if w]
        self.end = end

    @property
    def __self__(self):
        return {
            'words': [word.__self__ for word in self.words],
            'end': self.end,
        }

    def __repr__(self):
        return ' '.join([str(word) for word in self.words]) + self.end


class Word(Base):
    def __init__(self, word):
        self.word = word.strip()
        self.meta = {}

    @property
    def __self__(self):
        return self.__dict__

    def __json__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.word


f = File('sample0.txt')
f.read()

ss = f.sentences

s = ss[0]

ws = s.words

w = ws[0]
