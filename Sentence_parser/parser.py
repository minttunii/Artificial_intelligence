import argparse

import nltk


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
S -> NP VP
NP -> N | Det N | NP PP | Det AdjP N
VP -> V | V AdvP | VP ConjP | Adv V AdvP | Adv V
AdvP -> Adv | AdjP | PP | NP | PP AdvP
AdjP -> Adj | Adj AdjP
PP -> P NP
ConjP -> Conj VP | Conj NP VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('directory', help="load the data files from this directory", nargs="?")
    arg_parser.add_argument("-q", "--quiet", help="print just the noun phrase chunks (used by the grader)",
                            action="store_true")
    args = arg_parser.parse_args()

    # If filename specified, read sentence from file
    if args.directory is not None:
        with open(args.directory) as f:
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
    if not args.quiet:
        for tree in trees:
            tree.pretty_print()

            print("Noun Phrase Chunks")
            for np in np_chunk(tree):
                print(" ".join(np.flatten()))

    # Print just the noun phrase chunks
    else:
        np_set = set()
        for tree in trees:
            for np in np_chunk(tree):
                np_set.add(" ".join(np.flatten()))

        print("Noun Phrase Chunks")
        for np in sorted(np_set):
            print(np)


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = nltk.word_tokenize(sentence.lower())
    tokens = [ token for token in tokens if any(char.isalpha() for char in token)]
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NP_chunks = []
    tree = nltk.tree.ParentedTree.convert(tree)
    for chunk in tree.subtrees():
        if chunk.label() == 'N': 
            NP_chunks.append(chunk.parent())
    return NP_chunks

if __name__ == "__main__":
    main()
