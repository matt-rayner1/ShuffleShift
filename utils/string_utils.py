from collections import Counter

def vectorise_string(text):
    counts = Counter(c.lower() for c in text if c.isalpha())
    return [counts.get(chr(ord('a') + i), 0) for i in range(26)]
