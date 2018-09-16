from file_io.operations import get_excluded_words
from text_processing.operations import process_text
from database_models.models import Stats
from mongoengine import connect, DoesNotExist
from pymongo.errors import OperationFailure 
import argparse
import getpass

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

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, nargs=1, help='The name of the file containing data for learning')
args = parser.parse_args()
data_file = args.data[0]

excluded_words = get_excluded_words()

texts = []
with open(data_file, "r") as text_file:
    text = ""
    for line in text_file:
        print(repr(line))
        if not line=="\n":
            text += line.replace('\n', ' ')
        else:
            texts.append(text)
            text = ""
    texts.append(text)
    text = ""

processed_texts = []
for text in texts:
    processed_texts.append(process_text(text))

positive_texts = len(list(filter(lambda t: t[0] == '+', processed_texts)))
negative_texts = len(list(filter(lambda t: t[0] == '-', processed_texts)))

stats.modify(inc__negative=negative_texts)
stats.modify(inc__positive=positive_texts)
stats.save()