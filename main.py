from utils.argument_utils import parse_args, validate_args
from utils.string_utils import vectorise_string
from utils.nltk_utils import get_cfg_template
from solver.solver import generate
import pickle

def main():
    # STAGE 0: parse input args, valdiate, grab input text string
    args = parse_args() 
    input_string = validate_args(args)

    # STAGE 1: calculate letter budget 
    # no longer need to do this, just plug input_string in directly to generate()
    # letter_budget = vectorise_string(input_string)

    # STAGE 1.5: grab precomputed top 5k words dictionary data structure
    with open("./precompute/words_by_pos.pkl", "rb") as f:
        words_by_pos = pickle.load(f)

    # STAGE 2: grammar constrained sentence generation
    # [CONSTRAINED/MIRRORED CFG/POS APPROACH]
    # a) get cfg template of input sentence
    template = get_cfg_template(input_string)

    print(input_string)
    print(template)

    # b) solve it 
    solution = generate(input_string, words_by_pos)

    print(solution)


if __name__ == "__main__":
    main()
