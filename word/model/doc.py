from word.model.sample_word import SampleWord


class Doc(SampleWord):
    doc: str
    dictionary: str
    examples = list[str]

    def __init__(self, doc: str, dictionary: str, examples: list[str]):
        self.doc = doc
        self.dictionary = dictionary
        self.examples = examples
