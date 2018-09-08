import os

def get_excluded_words():
    dirname = os.path.dirname(__file__)
    EXCLUDE_FILES_PATH = '../exclude_lists'
    exclude_files = [os.path.join(dirname, EXCLUDE_FILES_PATH, f) for f in os.listdir(os.path.join(dirname, EXCLUDE_FILES_PATH))]
    exclude_words = []

    for exclude_file in exclude_files:
        with open(exclude_file, "r") as file:
            exclude_words += [word.rstrip('\n').lower() for word in file]

    exclude_words = sorted(exclude_words, key=lambda w: (len(w.split(' ')), len(w)), reverse=True)
    return exclude_words