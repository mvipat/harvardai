import nltk
import sys

from nltk.tokenize import word_tokenize


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
AP -> Adj | Adj AP | Det Adj
NP -> N | Det NP | AP N | N PP | N VP | N PP
PP -> P NP | N P | P VP
VP -> V | V NP | Conj VP | VP PP | Adv VP | P VP | PP VP | VP Adv | Conj VP
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
    ret_list = list()
    tokens = word_tokenize(sentence)
    for each_word in tokens:
        each_word = each_word.lower()
        if each_word.isalpha():
            ret_list.append(each_word)

    return ret_list

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    ret_list = list()
    for subtree in tree:
        #print(f"subtree {subtree}")
        if isinstance(subtree, nltk.Tree):
            #print(f"Node Label: {subtree.label()}")
            if subtree.label() == "NP":
                #print(f"found a child that is {child}")
                last_np_node = True
                for child_nodes in subtree:
                    if isinstance(child_nodes, nltk.Tree) and child_nodes.label() == "NP":
                        last_np_node = False
                        break
                
                if last_np_node:
                    if subtree not in ret_list:
                        print(f"is a np chunk {subtree}")
                        ret_list.append(subtree)
            else :
                np_chunk_list = np_chunk(subtree)  # Recursively call for children
                if len(np_chunk_list) != 0:
                    #print(f"np_chunk_list is {np_chunk_list}")
                    for item in np_chunk_list:
                        print(f"adding item {item}")
                        if item not in ret_list:
                            ret_list.append(item)
        else:
            a = True
            #print(f"Leaf: {subtree}")

    return ret_list

if __name__ == "__main__":
    main()
