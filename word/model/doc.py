from word.model.sample_word import SampleWord


class Doc(SampleWord):
    doc: str
    dictionary: str

    def __init__(self, doc: str, dictionary: str):
        self.doc = doc
        self.dictionary = dictionary
