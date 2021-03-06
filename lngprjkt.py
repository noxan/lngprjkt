import json


class Base(object):
    @property
    def __self__(self):
        return self.__dict__

    def __json__(self):
        return json.dumps(self.__self__)


class Manager(object):
    collection = {}
    model = None

    @classmethod
    def get(self, value):
        key = value.lower()
        if key not in self.collection:
            self.collection[key] = Word(value)
        return self.collection[key]

    @classmethod
    def set(self, key, value):
        self.collection[key] = value


class File(Base):
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        f = open(self.filename, 'r')
        content = f.read()

        content = content.replace('\n', '')
        content = content.replace('\r', '')

        for seperator in ['?', '!', ':']:
            content = content.replace(seperator, '.')

        separator = '.'

        self.sentences = [Sentence(s.strip(), separator) for s in content.split(separator) if s]

    def read(self):
        f = open(self.filename, 'r')
        content = f.read()

        self.sentences = []

        data = json.loads(content)

        for sentence in data['sentences']:
            for word in sentence['word']:
                words = [WordManager.get(word) for word, meta in word]
            end = sentence['end']
            self.sentences.append(Sentence(words, end))

        return data

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
        if isinstance(content, list):
            self.words = content
        else:
            content = content.replace(',', ' ')
            self.words = [WordManager.get(w) for w in content.split(' ') if w]
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
    NOUN, ADJECTIVE, VERB = range(3)

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


class WordManager(Manager):
    model = Word


f = File('sample0.json')
f.read()

ss = f.sentences

s = ss[0]

ws = s.words

w = ws[0]
