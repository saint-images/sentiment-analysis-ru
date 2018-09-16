from pprint import pprint
import json
from collections import defaultdict
from pymystem3 import Mystem
import re

def replace_all(text, words):
    for i in words:
        text = re.sub(r"\b%s\b" % i, '', text)
    return text

def process_text(text, exclude_words=[]):
    m = Mystem()
    lemmas = m.lemmatize(text)
    text = replace_all(''.join(lemmas[1:-1]), exclude_words)
    return((lemmas[0].strip(), text))