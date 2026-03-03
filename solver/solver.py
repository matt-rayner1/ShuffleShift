from utils.string_utils import vectorise_string
from utils.nltk_utils import get_cfg_template

TEMPLATES = {
    2: [
        ['N', 'V'],
        ['Pron', 'V'],
    ],
    3: [
        ['Det', 'N', 'V'],
        ['Pron', 'V', 'N'],
        ['N', 'V', 'Adv'],
        ['Det', 'Adj', 'N'],
    ],
    4: [
        ['Det', 'N', 'V', 'Adv'],
        ['Det', 'Adj', 'N', 'V'],
        ['Pron', 'V', 'Det', 'N'],
        ['Det', 'N', 'V', 'N'],
        ['Pron', 'V', 'Adj', 'N'],
    ],
    5: [
        ['Det', 'N', 'V', 'Prep', 'N'],
        ['Det', 'Adj', 'N', 'V', 'Adv'],
        ['Pron', 'V', 'Det', 'Adj', 'N'],
        ['Det', 'N', 'V', 'Det', 'N'],
        ['Pron', 'Modal', 'V', 'Det', 'N'],
    ],
    6: [
        ['Det', 'Adj', 'N', 'V', 'Prep', 'N'],
        ['Pron', 'V', 'Det', 'N', 'Prep', 'N'],
        ['Det', 'N', 'V', 'Det', 'Adj', 'N'],
        ['Pron', 'Modal', 'V', 'Det', 'Adj', 'N'],
        ['Det', 'N', 'Aux', 'V', 'Prep', 'N'],
    ],
}

class SolutionFound(Exception):
    pass

def order_template_by_constraint(template, letter_budget, words_by_pos):
    """Reorder template slots: most constrained (fewest viable candidates) first."""
    def viable_count(pos):
        return sum(
            1 for w in words_by_pos[pos]
            if all(b - v >= 0 for b, v in zip(letter_budget, w['vec']))
        )
    
    # return reordered template with original indices so we can reconstruct word order
    indexed = list(enumerate(template))
    indexed.sort(key=lambda x: viable_count(x[1]))
    return indexed  # list of (original_index, pos)

def compute_letter_rarity(letter_budget):
    """Letters with fewer occurrences in budget are rarer, score higher."""
    total = sum(letter_budget)
    if total == 0:
        return [0] * 26
    # invert frequency: rare letters score high, common letters score low
    return [1.0 / (count + 1) for count in letter_budget]

def candidate_rare_score(word_obj, rarity):
    """Higher score = word uses more rare letters."""
    return sum(count * rarity[i] for i, count in enumerate(word_obj['vec']))

def compute_pos_bounds(words_by_pos):
    """Precompute min/max word length per POS slot."""
    return {
        pos: (min(w['len'] for w in words), max(w['len'] for w in words))
        for pos, words in words_by_pos.items()
    }

def bounds_check(budget_sum, remaining_template, pos_bounds):
    """Return False if remaining budget can't possibly fill remaining slots."""
    if not remaining_template:
        return budget_sum == 0
    
    min_letters = sum(pos_bounds[pos][0] for pos in remaining_template)
    max_letters = sum(pos_bounds[pos][1] for pos in remaining_template)
    
    return min_letters <= budget_sum <= max_letters

def solve(letter_budget, ordered_slots, sentence_so_far, words_by_pos, pos_bounds):
    if not ordered_slots:
        if all(x == 0 for x in letter_budget):
            # reorder words back to original template order
            result = [word for _, word in sorted(sentence_so_far, key=lambda x: x[0])]
            raise SolutionFound(result)
        return

    budget_sum = sum(letter_budget)
    if not bounds_check(budget_sum, [pos for _, pos in ordered_slots], pos_bounds):
        return

    (original_idx, current_pos), remaining_slots = ordered_slots[0], ordered_slots[1:]
    candidates = words_by_pos[current_pos]

    rarity = compute_letter_rarity(letter_budget)
    sorted_candidates = sorted(candidates, key=lambda w: candidate_rare_score(w, rarity), reverse=True)

    for word_obj in sorted_candidates:
        new_budget = [b - v for b, v in zip(letter_budget, word_obj['vec'])]
        if any(x < 0 for x in new_budget):
            continue
        solve(new_budget, remaining_slots, sentence_so_far + [(original_idx, word_obj['word'])], words_by_pos, pos_bounds)

def generate(input_sentence, words_by_pos):
    pos_bounds = compute_pos_bounds(words_by_pos)
    budget = vectorise_string(input_sentence)
    word_count = len(input_sentence.split())
    
    templates = TEMPLATES.get(word_count, [])
    if not templates:
        print(f"No templates for word count {word_count}")
        return None

    for template in templates:
        ordered_slots = order_template_by_constraint(template, budget, words_by_pos)
        try:
            solve(budget, ordered_slots, [], words_by_pos, pos_bounds)
        except SolutionFound as e:
            print(f"Solution found with template: {template}")
            return e.args[0]
    
    print("No solution found across all templates")
    return None
