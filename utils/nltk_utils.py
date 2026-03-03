import nltk
from nltk import pos_tag, word_tokenize

nltk.download("averaged_perceptron_tagger_eng")
nltk.download("punkt_tab")

# Penn Treebank -> your CFG tags
PTB_TO_CFG = {
    'NN': 'N', 'NNS': 'N', 'NNP': 'N', 'NNPS': 'N',
    'VB': 'V', 'VBD': 'V', 'VBG': 'V', 'VBN': 'V', 'VBP': 'V', 'VBZ': 'V',
    'JJ': 'Adj', 'JJR': 'Adj', 'JJS': 'Adj',
    'RB': 'Adv', 'RBR': 'Adv', 'RBS': 'Adv',
    'DT': 'Det',
    'IN': 'Prep',
    'CC': 'Conj',
    'PRP': 'Pron', 'PRP$': 'Pron', 'WP': 'Pron', 'WP$': 'Pron',
    'MD': 'Modal',
}

def get_cfg_template(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    
    template = []
    for word, ptb_tag in tagged:
        cfg_tag = PTB_TO_CFG.get(ptb_tag)
        if cfg_tag:
            template.append(cfg_tag)
        # silently skip punctuation, numbers, unknowns
    
    return template

