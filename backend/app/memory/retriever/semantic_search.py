from app.memory.config import TOP_K


class SemanticSearch:

    def __init__(self, store):
        self.store = store

    def search(self, vector, user_id):
        """
        Perform semantic search with user-level filtering
        """
        return self.store.search(vector, user_id, TOP_K)