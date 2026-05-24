"""TF-IDF exemplar retrieval for Targem."""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from targem.corpus import CorpusPair


class TFIDFRetriever:
    """Retrieves the most similar corpus pairs for a query using TF-IDF cosine similarity."""

    def __init__(self, pairs: list[CorpusPair]) -> None:
        self._pairs = pairs
        self._vectorizer = TfidfVectorizer(strip_accents="unicode", lowercase=True)
        corpus_texts = [p.english for p in pairs]
        self._matrix = self._vectorizer.fit_transform(corpus_texts)

    def retrieve(self, query: str, k: int = 3) -> list[CorpusPair]:
        """Return the top-k corpus pairs most similar to the query."""
        k = min(k, len(self._pairs))
        query_vec = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self._matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:k]
        return [self._pairs[i] for i in top_indices]
