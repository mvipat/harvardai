import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    print(f"input one_gene {one_gene} two_genes {two_genes} have_trait {have_trait}")
    # Initialize probability dictionary
    ret_probabilities = dict()
    for person in people:
        ret_probabilities[people[person]["name"]] = 1

    for person in people:
        trait_value = False
        if people[person]["name"] in have_trait:
            trait_value = True
        
        copies_of_gene = get_number_of_genes( people[person]["name"],one_gene,two_genes)
        print(f"person {person} copies_of_gene {copies_of_gene} trait_value {trait_value}")
        
        if people[person]['mother'] is None and  people[person]['father'] is None:
            ret_probabilities[people[person]["name"]] = PROBS["gene"][copies_of_gene] * PROBS["trait"][copies_of_gene][trait_value]
        else :
            copies_of_fathers_gene = get_number_of_genes(people[person]["father"],one_gene,two_genes)
            copies_of_mothers_gene = get_number_of_genes(people[person]["mother"],one_gene,two_genes)
            mother_trait = people[person]["mother"] in have_trait
            father_trait = people[person]["father"] in have_trait

            print(f"copies_of_fathers_gene {copies_of_fathers_gene} \
                    copies_of_mothers_gene {copies_of_mothers_gene} \
                    mother_trait {mother_trait} father_trait {father_trait}")

            father_probability = get_probability(copies_of_fathers_gene)
            mother_probability = get_probability(copies_of_mothers_gene)
            print(f"father_probability {father_probability} mother_probability {mother_probability}")

            if copies_of_gene == 2:
                prob_value = father_probability * mother_probability
            elif copies_of_gene == 1:
                prob_value = father_probability * (1-mother_probability) + mother_probability * (1-father_probability)
            else :
                prob_value = (1-mother_probability) * (1-father_probability)

            print(f"prob_value before multiplying trait {prob_value}")
            prob_value *= PROBS["trait"][copies_of_gene][trait_value]
            print(f"prob_value after multiplying trait {prob_value}")
            
            ret_probabilities[people[person]["name"]] = prob_value

    prob_value = 1
    for name,prob in ret_probabilities.items():
        print(f"individual probability {name} {prob}")
        prob_value *= prob

    print(f"joint_probability {prob_value}")

    return prob_value

def get_probability(mother_father):
    """
    This function accepts 
    """
    
    prob_value = 1
    if mother_father == 0:
        prob_value = PROBS["mutation"]
    elif mother_father == 1:
        #chance = 0.5
        #prob_value = chance - PROBS["mutation"]
        return 0.5
    elif mother_father == 2:
        chance = 1
        prob_value = chance * (1-PROBS["mutation"])
    else :
        raise ValueError(f"Wrong number of genes {mother_father}")

    return prob_value
    
def get_number_of_genes(person,one_gene,two_genes):
    """
    This function accepts person, one_gene and two_genes lists and determines how many genes the person has
    """
    copies_of_gene = 0
    if person in one_gene:
        copies_of_gene = 1

    if person in two_genes:
        copies_of_gene = 2

    return copies_of_gene

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person,probs in probabilities.items():
        copies_of_gene = get_number_of_genes(person,one_gene,two_genes)
        trait_value = False
        if person in have_trait:
            trait_value = True

        print(f"person {person} copies_of_gene {copies_of_gene} trait_value {trait_value}")
        before_updating_gene_prob = probabilities[person]["gene"][copies_of_gene]
        before_updating_trait_prob = probabilities[person]["trait"][trait_value]

        print(f"before gene {before_updating_gene_prob} trait {before_updating_trait_prob} prob {p}")

        probabilities[person]["gene"][copies_of_gene] += p
        
        probabilities[person]["trait"][trait_value] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total_gene_sum = 0
        for gene,gene_probability in probabilities[person]["gene"].items():
            total_gene_sum += gene_probability

        print(f"person {person} total_gene_sum {total_gene_sum}")
        for gene,gene_probability in probabilities[person]["gene"].items():
            print(f"gene {gene} gene_probability {gene_probability}")
            if total_gene_sum is None or total_gene_sum == 0:
                probabilities[person]["gene"][gene] = gene_probability
            else :
                probabilities[person]["gene"][gene] = gene_probability / total_gene_sum

        total_trait_sum = 0
        for trait,trait_probability in probabilities[person]["trait"].items():
            total_trait_sum += trait_probability

        for trait,trait_probability in probabilities[person]["trait"].items():
            if total_trait_sum is None or total_trait_sum == 0:
                probabilities[person]["trait"][trait] = trait_probability
            else:
                probabilities[person]["trait"][trait] = trait_probability / total_trait_sum

if __name__ == "__main__":
    main()
