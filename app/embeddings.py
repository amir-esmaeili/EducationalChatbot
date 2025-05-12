from sentence_transformers import SentenceTransformer
import numpy as np
import json
import faiss


class ContentEmbedder:
    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        self.content = []
        self.embeddings = None
        self.index = None

    def load_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = json.load(f)

        # Create text chunks for more precise retrieval
        self.chunks = []
        for item in self.content:
            sentences = item['content'].split('. ')
            for i in range(0, len(sentences), 2):
                chunk = '. '.join(sentences[i:i + 2])
                if chunk:
                    self.chunks.append({
                        'content_id': item['id'],
                        'title': item['title'],
                        'text': chunk,
                        'full_content': item['content']
                    })

        texts = [chunk['text'] for chunk in self.chunks]
        self.embeddings = self.model.encode(texts)

        vector_dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(vector_dimension)
        self.index.add(np.array(self.embeddings).astype('float32'))

    def search(self, query, top_k=1):
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.chunks[idx])

        return results
