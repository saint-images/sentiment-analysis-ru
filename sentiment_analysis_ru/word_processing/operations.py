from collections import defaultdict

def get_word_data(text):
    words = defaultdict(int)

    for word in str.split(text, ' '):
        word = word.lower()
        for char in ['.', ',', '-', '"', '!', '?', '\n']:
            word = word.replace(char, '')
        if word:
            words[word] += 1

    return dict(words)