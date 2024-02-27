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

def inherit_prob(parent_name, one_gene, two_genes):
    """
    joint_probability helper function
    Returns the probability of a parent giving a copy of the mutated gene to their child.
    """
    if parent_name in two_genes:
        return 1 - PROBS['mutation']
    elif parent_name in one_gene:
        return 0.5
    else:
        return PROBS['mutation']
    
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
    def get_prob_gene(num_genes):
        return PROBS["gene"][num_genes]

    def get_prob_trait(num_genes, trait):
        return PROBS["trait"][num_genes][trait]

    joint_prob = 1.0

    for person, data in people.items():
        mother = data['mother']
        father = data['father']

        if person in one_gene:
            genes = 1
        elif person in two_genes:
            genes = 2
        else:
            genes = 0

        has_trait = person in have_trait

        # If person has no parents, use gene probability directly
        if mother is None and father is None:
            joint_prob *= get_prob_gene(genes) * get_prob_trait(genes, has_trait)
        else:
            # Determine probability of inheriting genes from parents
            mother_prob = inherit_prob(mother, one_gene, two_genes)
            father_prob = inherit_prob(father, one_gene, two_genes)
            child_prob = 1

            if genes == 0:
                child_prob *= (1 - mother_prob) * (1 - father_prob) 
            elif genes == 1:
                child_prob *= (1 - mother_prob) * father_prob + mother_prob * (1 - father_prob) 
            else:
                child_prob *= mother_prob * father_prob 

            child_prob *= get_prob_trait(genes, has_trait) 
            joint_prob *= child_prob 

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        num_genes = 0
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2

        has_trait = False
        if person in have_trait:
            has_trait = True

        probabilities[person]["gene"][num_genes] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for distribution_type in probabilities[person]:
            distribution = probabilities[person][distribution_type]
            total_probability = sum(distribution.values())

            # Normalize the distribution
            for key in distribution:
                distribution[key] /= total_probability



if __name__ == "__main__":
    main()
