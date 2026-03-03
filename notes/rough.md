# Idea:

given an input sentence
e.g. "Tom Marvolo Riddle"
generate a completely new sentence from the constituent letters (letter "budget")
-> "I am lord voldemort"

# Challenges 
This is NP-hard-ish. Involving exploring possible branches to generate a gramatically correct sentence. 

Extremely easy to verify. Literally just count up all the letters compared to the input for equivalence.

Originally, I was thinking of bruteforcing the problem, generating a series of candidate word sets from the input letter budget, and then verifying it for gramatical sense. 

However, I quickly discovered that this was an exponential computation, O(n^n) ish. 

Not that I ever really knew or needed to know about big O notation before now, but in this case its actually useful for once. 

I need ways to constrain this problem, which is where CFG (Context-Free Grammar) could be incredibly helpful

If i scaffold a sentence structure FIRST, and then go through the candidate generation, then ideally, by the time a sentence has been computed, it has already been verified for gramatical correctness 

I'm also choosing to constrain maximum input size to 200 characters to begin with, but i might have to tweak this over time. 

# Plan of attack 
here are the stages to go through 

## STAGE 0
Input validation/boilerplate 

probs gonna be run like 

`python main.py --file input.txt`

or 

`python main.py --text "Example input text sentence"`

limit to 200 chars, validate that its text, bosh. 

## STAGE 1
Count up all letters (letter budget) in an input text, 

i.e. ` letter_budget = {a: 5, b: 2, ..., z: 1}`

trivial. literally a oneliner 

apparently better to just use an integer list instead. 

i.e. `letter_budget = [5, 2, ..., 1]`

index implies a/b/c. "a" at position 0, "b" is position 1 etc 

## STAGE 1.5 
PRECOMPUTE DICTIONARY DATA STRUCTURE 

We are gonna need a top words dictionary to use in our candidate sentence generation. 

Im thinking the nltp top 5k should probably do fine. 5k might even be too much but its an actual number to try first 

originally, i was thinking the structure would be by word 
```
{
    "dog": {
        "pos": "N", 
        "vec": [0, 0, 0, 1, ...]
    }
}
```

BUT, since we've decided to constrain by gramatical structure, during the generation process we can specify "now we need a noun"

something looking like generate_word(budget, "noun")

So, its probably best to precompute a different form of data structure, POS-first organised. 

So we can make the data structure by noun, verb, etc:

```
words_by_pos = {
    "N": [word_obj1, word_obj2],
    "V": [...],
    "Adj": [...],
    ...
}
```

The word_objs themselves can contain the word itself, and the letter vectors 

```
word_obj = {
    "word": "dog",
    "vec": [0, 0, 0, 1, ...],
    "len": 3,
}
```

as mentioned at the start, this data structure only needs to be precomputed once, we dont wanna be doing this every runtime lol 

then we can pickle it and retrieve it on actual solver runs.

## STAGE 2 
GRAMMAR CONSTRAINED SEARCH

Here's where it gets spicy. 

First, still not sure what to choose here, we need to decide the grammar structure of the generation. 
either: 

a) fixed small CFG (how do i choose whats appropriate, especially if the sentence is tiny vs the full 200 characters)

b) input-derived POS template - could just analyse the input sentence structure, and constrain the entire generation to the exact input structure 

either way, the CFG structure needs to be defined properly here, and then we can go on to actual sentence generation

ok so ive messed around with b) and its a bit too constrained, a) as a single CFG template also too constrained, looks like having a pool of CFGs to iterate through leads to more solves.

so lets assume we have a CFG structure to use. now we generate sentences 

we have our input letter budget, and a grammar state

something like 

`search(letter_budget, grammar_state)`

there are some good branch pruning things to consider right away

a) we can vector subtract our dict structure word vec, from our letter_budget vec. anything that goes negative we can immediately reject. 

b) memoisation: we gotta be caching certain states so we dont have to recompute every time. 

c) rare letters first: no point generating words from common letters, then findiing that we cant fit the "x" characters; we've just burned through computation down a shit branch for no reason.

d) word count bounds: if the remaining letters < minimum possible remaining slots -> prune that shit. 
   if too many slots left for remaining letters (how do we calculate this case?) -> prune. 

e) early termination: we only need 1 solution. once we've hit a correct sentence generation, we've done it. (early on i was thinking to generate multiple candidate sentences but due to CFG we can just do one candidate!)

## STAGE 3 
just output the result. ez. 



# misc notes 
## day 1 
we got a 67% solve rate based on some random small sentences. its a start 

need to add more tests, not just end to end/solver tests 

get_cfg_template is pretty innacurate - first priority should probs be fixing this. 

wait actually do we even need get_cfg_template anymore? if we aren't putting it on rails (getting cfg template for input -> forcing output to adhere to that) then probably isnt useful anymore. 

better option is counting the words in the input, then having a lookup table for possible CFG templates for that specific amount of words. 

Solver is messy and i'm tripping myself up. go to pen and paper tomorrow, revisit branch pruning strats, theres some others that are useful. 

claude was a good rubber duck that talked back. takes actual effort to not just say "ok do the next bit", honestly, thats what tripped me up. do the right thing and take it to ground, understand it better it will serve you in the long run. yea slightly too "vibed" today, not completely but enough that im getting a bit behind on the solver implementation (and tests but its tests who likes actually writing those)

oh yea figure out testing/environment bs cause actually getting pytest to run was a bitch, and quite rushed. 

part of fixing the CFG output is our precompute. i think we have some mismatches in our words_by_pos.pkl. worth a revisit/some more analysis. at least the general principle is there and we have a working compute_wordlist.py

git push at the end of each day
