from app.embeddings import ContentEmbedder


class ContentRetriever:
    def __init__(self, content_path):
        self.embedder = ContentEmbedder()
        self.embedder.load_content(content_path)

    def get_relevant_content(self, query):
        results = self.embedder.search(query, top_k=1)
        if results:
            return results[0]
        return None
