from file_io.operations import get_excluded_words
import argparse

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