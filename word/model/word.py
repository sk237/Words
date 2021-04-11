from word.model.sample_word import SampleWord


class Word(SampleWord):
    word: str

    def __init__(self, word):
        self.word = word
