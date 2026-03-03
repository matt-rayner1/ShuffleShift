import sys
import os


import pytest 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.solver import generate
import pickle

@pytest.fixture(scope="module")
def words_by_pos():
    with open("precompute/words_by_pos.pkl", "rb") as f:
        return pickle.load(f)

TEST_SENTENCES = [
    # 2 words
    "dogs bark",
    "birds sing",
    "time flies",
    "cats sleep",
    "rain falls",
    "stars shine",
    "wind blows",
    "hearts break",

    # 3 words
    "the dog runs",
    "she loves him",
    "birds fly south",
    "he runs fast",
    "cats hate water",
    "time heals wounds",
    "children love candy",
    "snow falls softly",
    "fire burns bright",
    "music fills rooms",

    # 4 words
    "the cat sat",
    "she runs very fast",
    "he loves the rain",
    "dogs chase their tails",
    "birds sing at dawn",
    "the moon shines bright",
    "children laugh and play",
    "old men forget easily",
    "great minds think alike",
    "good dogs sit still",

    # 5 words
    "the dog runs very fast",
    "she walks in the rain",
    "he reads every single day",
    "cats sleep in the sun",
    "birds nest in tall trees",
    "the wind blows from north",
    "good things come to those",
    "old habits die very hard",
    "small birds eat tiny seeds",
    "dark clouds fill the sky",
    "the child runs toward home",
    "cold water fills the glass",

    # 6 words
    "the old dog runs very fast",
    "she walks alone in the rain",
    "he reads books every single day",
    "small cats sleep in warm beds",
    "tall birds nest in old trees",
    "the cold wind blows from north",
    "bright stars shine in dark skies",
    "young children play in green fields",
    "the brave man fights for freedom",
    "cold fresh water fills the glass",
    "the sad girl sits by herself",
    "strong winds blow the leaves away",
]

@pytest.mark.parametrize("sentence", TEST_SENTENCES)
def test_generate_finds_solution(sentence, words_by_pos):
    result = generate(sentence, words_by_pos)
    assert result is not None, f"No solution found for: '{sentence}'"
    assert len(result) == len(sentence.split()), f"Wrong word count for: '{sentence}'"

def test_generate_exhausts_budget(words_by_pos):
    """Verify output uses exactly the same letters as input."""
    from utils.string_utils import vectorise_string
    for sentence in TEST_SENTENCES:
        result = generate(sentence, words_by_pos)
        if result is None:
            continue
        input_vec = vectorise_string(sentence)
        output_vec = vectorise_string(" ".join(result))
        assert input_vec == output_vec, (
            f"Budget mismatch for '{sentence}'\n"
            f"  input:  {input_vec}\n"
            f"  output: {output_vec}"
        )

def test_solution_rate(words_by_pos):
    """Track overall success rate — soft target of 80%."""
    solved = sum(1 for s in TEST_SENTENCES if generate(s, words_by_pos) is not None)
    rate = solved / len(TEST_SENTENCES)
    print(f"\nSolution rate: {solved}/{len(TEST_SENTENCES)} ({rate:.0%})")
    assert rate >= 0.8, f"Solution rate too low: {rate:.0%}"
