# summarizer_extractive.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Ensure NLTK data is available (punkt + punkt_tab for newer NLTK)
def _ensure_nltk():
    try:
        import nltk

        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")

        # For NLTK >= 3.8.1, punkt metadata is split out
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            # Older NLTK won’t have this; ignore failures here
            try:
                nltk.download("punkt_tab")
            except Exception:
                pass
    except Exception:
        # If nltk import fails, sumy’s own tokenizer should still work;
        # but LexRank quality may drop slightly.
        pass

def _summarize_once(text: str, sentences_count: int, language: str = "english") -> str:
    _ensure_nltk()
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LexRankSummarizer()
    sentences = summarizer(parser.document, max(1, sentences_count))
    return " ".join(str(s) for s in sentences)

def summarize_extractive(text: str, sentences_count: int | None = None, language: str = "english") -> str:
    text = (text or "").strip()
    if not text:
        return ""
    words = text.split()
    n_words = len(words)

    if sentences_count is None:
        sentences_count = 3 if n_words < 120 else 5 if n_words < 400 else 7 if n_words < 1000 else 9

    if n_words <= 800:
        return _summarize_once(text, sentences_count, language)

    # Chunk long docs, summarize parts, then summarize the combined text
    chunk_size = 800
    partials = []
    for i in range(0, n_words, chunk_size):
        chunk_text = " ".join(words[i:i + chunk_size])
        partials.append(_summarize_once(chunk_text, 3, language))
    combined = " ".join(partials)
    return _summarize_once(combined, sentences_count, language)