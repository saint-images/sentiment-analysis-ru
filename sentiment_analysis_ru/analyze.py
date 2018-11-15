import argparse
import getpass
import math
import re

from mongoengine import DoesNotExist, connect
from pymongo.errors import OperationFailure
from tqdm import tqdm

from database_models.models import Stats, Word
from file_io.operations import get_excluded_words
from text_processing.operations import process_text
from word_processing.operations import get_word_data

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, nargs=1, help='The name of the file containing the text to be analyzed')
args = parser.parse_args()
data_file = args.data[0]

print('Atlas credentials:')
db_username = input('Username: ')
db_password = getpass.getpass()

connect(db='SentimentAnalysis', host=f'mongodb+srv://{db_username}:{db_password}@sentimentanalysis-hpnfo.mongodb.net/SentimentAnalysis?retryWrites=true')
try:
    stats = Stats.objects.get()
except DoesNotExist:
    stats = Stats()
    stats.save()
except OperationFailure:
    print('Database authentication failed!')
    exit()

excluded_words = get_excluded_words()

text = ""
with open(data_file, "r") as text_file:
    for line in text_file:
        if not line=="\n":
            text += line.replace('\n', ' ')

processed_text = process_text(text, exclude_words=excluded_words, analyze=True)
words = []
for word in str.split(processed_text, ' '):
        if word.startswith('@') or word.startswith('#') or word == 'не': # Twitter stuff
            continue
        word = re.sub('[^А-Яа-я]', '', word.lower().replace('ё', 'е'))
        words.append(word)

words = [word for word in words if not word == ""]

sum = 0
for word in words:
    try:
        word_entry = Word.objects(word=word).get()
        count = words.count(word)
        positive_texts = stats.positive
        negative_texts = stats.negative
        positive_count = word_entry.positive
        negative_count = word_entry.negative
        try:
            pos_mult = positive_count/positive_texts
        except ZeroDivisionError:
            pos_mult = 0
        try:
            neg_mult = negative_count/negative_texts
        except ZeroDivisionError:
            neg_mult = 0
        weight = count * pos_mult - count * neg_mult
        sum += weight
        print(f'{word}: {weight}')
    except DoesNotExist:
        print("Slow down here mate: ", word)

print("Sum: ", sum)
