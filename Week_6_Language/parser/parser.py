import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
    S -> NP VP | NP VP Adv | S Conj S | VP | NP
    AP -> Adj | Adj AP 
    NP -> N | Det N | Det AP N | NP PP | NP AP
    PP -> P | P NP
    VP -> V | V NP | V NP | V PP | Adv VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lower_sentence = sentence.lower()
    tokenized_sentence = nltk.word_tokenize(lower_sentence)
    non_alphabetic = []
    for word in tokenized_sentence:
        if not word.isalpha():
            non_alphabetic.append(word)
    for word in non_alphabetic:
        tokenized_sentence.remove(word)
    return tokenized_sentence



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # print(tree)
    found = []
    for el in tree:
        if type(el) is str:
            return []
        if el.label() == 'NP':
            if np_chunk(el) == []:
                found.append(el)
            else:
                found.extend(np_chunk(el))
        else:
            found.extend(np_chunk(el))
    return found


if __name__ == "__main__":
    main()
