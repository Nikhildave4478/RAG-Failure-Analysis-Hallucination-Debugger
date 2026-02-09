import random

class FailureInjector:
    def __init__(self, mode=None):
        """
        mode:
        - None (no failure)
        - drop_chunks
        - shuffle_context
        - truncate_context
        """
        self.mode = mode

    def apply(self, docs):
        if self.mode is None:
            return docs

        if self.mode == "drop_chunks":
            return docs[:1]   # remove most context

        if self.mode == "shuffle_context":
            shuffled = docs[:]
            random.shuffle(shuffled)
            return shuffled

        if self.mode == "truncate_context":
            for d in docs:
                d.page_content = d.page_content[:100]
            return docs

        return docs
