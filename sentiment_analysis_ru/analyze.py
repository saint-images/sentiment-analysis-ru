from database_models.models import Stats, Word
from mongoengine import connect, DoesNotExist
from pymongo.errors import OperationFailure
from tqdm import tqdm
import argparse
import getpass

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