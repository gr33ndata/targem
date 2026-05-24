"""Tests for TF-IDF exemplar retrieval."""

from targem.corpus import CorpusPair
from targem.retrieval import TFIDFRetriever

PAIRS = [
    CorpusPair(english="The cat sat on the mat.", egyptian_arabic="القطة جلست على الحصيرة."),
    CorpusPair(english="Football is a popular sport.", egyptian_arabic="الكورة رياضة مشهورة."),
    CorpusPair(english="She went to the market to buy food.", egyptian_arabic="راحت السوق تشتري أكل."),
    CorpusPair(english="The economy is struggling with inflation.", egyptian_arabic="الاقتصاد بيعاني من التضخم."),
    CorpusPair(english="He loves reading books every evening.", egyptian_arabic="بيحب يقرا كتب كل مساء."),
]


def test_retrieve_returns_k_results():
    retriever = TFIDFRetriever(PAIRS)
    results = retriever.retrieve("cat and mat", k=3)
    assert len(results) == 3


def test_retrieve_most_similar_first():
    retriever = TFIDFRetriever(PAIRS)
    results = retriever.retrieve("football match sport", k=1)
    assert "Football" in results[0].english


def test_retrieve_k_larger_than_corpus():
    retriever = TFIDFRetriever(PAIRS)
    results = retriever.retrieve("test query", k=100)
    assert len(results) == len(PAIRS)


def test_retrieve_returns_corpus_pairs():
    retriever = TFIDFRetriever(PAIRS)
    results = retriever.retrieve("economy inflation prices", k=2)
    assert all(isinstance(r, CorpusPair) for r in results)


def test_retrieve_single_pair_corpus():
    single = [CorpusPair(english="hello world", egyptian_arabic="أهلا بالعالم")]
    retriever = TFIDFRetriever(single)
    results = retriever.retrieve("hello", k=3)
    assert len(results) == 1
