# Compact fuzzy matching replacement for fuzzywuzzy (no dependencies)
# Provides: partial_ratio, extract

def partial_ratio(a, b):
    """
    Returns a similarity score between 0 and 100 based on the best matching substring.
    """
    a = str(a)
    b = str(b)
    if not a or not b:
        return 0
    if a == b:
        return 100
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    max_score = 0
    len_short = len(shorter)
    for i in range(len(longer) - len_short + 1):
        window = longer[i:i+len_short]
        matches = sum(1 for x, y in zip(shorter, window) if x == y)
        score = int(100 * matches / len_short)
        if score > max_score:
            max_score = score
        if max_score == 100:
            break
    return max_score

def extract(query, choices, limit=5, scorer=partial_ratio):
    """
    Returns a list of (choice, score) tuples, sorted by score descending.
    Removes duplicate choices (keeps the first occurrence).
    """
    seen = set()
    unique_choices = []
    for choice in choices:
        if choice not in seen:
            unique_choices.append(choice)
            seen.add(choice)
    results = []
    for choice in unique_choices:
        score = scorer(query, choice)
        results.append((choice, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:limit] 