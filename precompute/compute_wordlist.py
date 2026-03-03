# IMPORTS
# global
import sys
import os
from wordfreq import top_n_list
import nltk 
from nltk.corpus import wordnet 
from collections import defaultdict
import pickle

# local
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.string_utils import vectorise_string

# download whats needed 
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("wordnet")

# LOCAL HELPER FNS
def make_word_obj(word):
    return word_obj_index.get(word, {
        "word": word, 
        "vec": vectorise_string(word),
        "len": len(word),
    })

def get_cfg_pos(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return None
    return WN_POS_MAP.get(synsets[0].pos(), None)

# CONSTANTS
TOP_N_VALUE = 5000
TOP_N_BUFFER = 2000 # we need to exclude emojis and numbers from the raw_list, this is our breathing room

# maybe not exhaustive but its good enough
FUNCTION_WORDS = {
    "Det":   ["the", "a", "an", "this", "that", "these", "those", "my", "your", "his", "her", "its", "our", "their", "some", "any", "each", "every", "no"],
    "Prep":  ["in", "on", "at", "by", "for", "with", "about", "against", "between", "through", "during", "before", "after", "above", "below", "from", "up", "down", "to", "of", "off", "over", "under", "into", "onto"],
    "Conj":  ["and", "but", "or", "nor", "so", "yet", "although", "because", "since", "unless", "while", "whereas"],
    "Pron":  ["i", "you", "he", "she", "it", "we", "they", "me", "him", "us", "them", "who", "what", "which", "myself", "yourself"],
    "Modal": ["can", "will", "would", "should", "could", "may", "might", "must", "shall", "ought"],
    "Aux":   ["is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did"],
}

# flatten set of FUNCTION_WORDS to exclude from wordnet tagging
ALL_FUNCTION_WORDS = {w for words in FUNCTION_WORDS.values() for w in words}

# wordnet POS -> CFG tag
WN_POS_MAP = {
    'n': 'N',
    'v': 'V',
    'a': 'Adj',
    's': 'Adj',  # adjective satellites
    'r': 'Adv',
}

# grab top n wordlist from wordfreq
raw_list = top_n_list('en', TOP_N_VALUE + TOP_N_BUFFER)

top_n = [word for word in raw_list if word.isalpha()][:TOP_N_VALUE]

# create word_objs list for top_n
word_objs = [
    {
        "word": word, 
        "vec": vectorise_string(word),
        "len": len(word),
    }
    for word in top_n
]

# index word_objs by word (quick lookup)
word_obj_index = {w["word"]: w for w in word_objs}

# set up empty dict
words_by_pos = defaultdict(list)

# tag content words with wordnet (skip anything in FUNCTION_WORDS)
for word_obj in word_objs:
    word = word_obj["word"]
    if word in ALL_FUNCTION_WORDS:
        continue
    pos = get_cfg_pos(word)
    if pos:
        words_by_pos[pos].append(word_obj)

# add fn words 
for pos, words in FUNCTION_WORDS.items():
    for word in words:
        words_by_pos[pos].append(make_word_obj(word))

# zombie print code for having a peek 
# for pos, words in sorted(words_by_pos.items()):
#     print(f"\n[{pos}] ({len(words)} words)")
#     for w in words:
#         print(f"  {w['word']:<20} len={w['len']}  vec={w['vec']}")
#
# total = sum(len(words) for words in words_by_pos.values())
# print(f"\nTotal words across all POS: {total}")

# pickle this mf
with open("./precompute/words_by_pos.pkl", "wb") as f:
    pickle.dump(words_by_pos, f)

print("saved ./precompute/words_by_pos.pkl")
