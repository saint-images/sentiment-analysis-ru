from collections import defaultdict
import re

def get_word_data(text):
    words = defaultdict(int)

    for word in str.split(text, ' '):
        word = re.sub('[^А-Яа-я]', '', word.lower().replace('ё', 'е'))
        if word and not word == 'не':
            words[word] += 1

    return dict(words)