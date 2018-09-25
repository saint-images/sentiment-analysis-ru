from pymystem3 import Mystem
import re

def replace_all(text, words):
    for i in words:
        text = re.sub(r"\b%s\b" % i, '', text)
    return text

def process_text(text, exclude_words=[]):
    m = Mystem()
    lemmas = m.lemmatize(text)
    text = replace_all(''.join(lemmas[1:-1]), exclude_words) # the last element is always \n for some reason
    return((lemmas[0].strip(), text))
