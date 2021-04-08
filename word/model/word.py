class Word:
    key: str
    description: str
    examples = list[str]

    def __init__(self, key: str, description: str, examples: list[str]):
        self.key = key
        self.description = description
        self.examples = examples
