import argparse
import getpass
from collections import defaultdict

from mongoengine import DoesNotExist, connect
from pymongo.errors import OperationFailure
from tqdm import tqdm

from database_models.models import Stats, Word
from file_io.operations import get_excluded_words
from text_processing.operations import process_text
from word_processing.operations import get_word_data


def merge_dicts(dict1, dict2):
    for k, v in dict2.items():
        dict1[k] += v
    
    return dict1

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, nargs=1, help='The name of the file containing data for learning')
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

texts = []
with open(data_file, "r") as text_file:
    with open('data_log.txt', 'a') as log_file:
        text = ""
        for line in text_file:
            log_file.write(line)
            if not line=="\n":
                text += line.replace('\n', ' ')
            else:
                texts.append(text)
                text = ""
        texts.append(text)
        log_file.write('\n')
        log_file.write('\n')
        text = ""

processed_texts = []
print('Processing texts...')
for text in tqdm(texts):
    processed_texts.append(process_text(text, exclude_words=excluded_words))

positive_texts = len(list(filter(lambda t: t[0] == '+', processed_texts)))
negative_texts = len(list(filter(lambda t: t[0] == '-', processed_texts)))

stats.modify(inc__negative=negative_texts)
stats.modify(inc__positive=positive_texts)
stats.save()

positive_words = defaultdict(int)
negative_words = defaultdict(int)

for text in processed_texts:
    words = get_word_data(text[1])
    if text[0] == '-':
        negative_words = merge_dicts(negative_words, words)
    elif text[0] == '+':
        positive_words = merge_dicts(positive_words, words)
    else:
        print('Tone not specified!')
        continue

print('Saving positive words to the database...')
for word, amount in tqdm(positive_words.items()):
    try:
        word_entry = Word.objects.get(word=word)
    except DoesNotExist:
        word_entry = Word(word)
        word_entry.save()
    word_entry.modify(inc__positive=1)
    word_entry.save()

print('Saving negative words to the database...')
for word, amount in tqdm(negative_words.items()):
    try:
        word_entry = Word.objects.get(word=word)
    except DoesNotExist:
        word_entry = Word(word)
        word_entry.save()
    word_entry.modify(inc__negative=1)
    word_entry.save()

open(data_file, "w").close()
