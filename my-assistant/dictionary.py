def meaning(word):
    try:
        from nltk.corpus import wordnet
    except ImportError:
        return "I couldn't find a meaning for {word} because the NLTK library is not installed."

    synsets = wordnet.synsets(word)
    if not synsets:
        return f"I couldn't find a meaning for {word}."
    return f"{word}: {synsets[0].definition()}"


def spell(word):
    return "-".join(letter.upper() for letter in word if letter.isalpha())
