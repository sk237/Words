from word.model.sample_word import SampleWord


class Examples(SampleWord):
    examples: list[str]

    def __init__(self, examples):
        self.examples = examples
