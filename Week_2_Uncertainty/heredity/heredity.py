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
    # print(people)
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

def prob_of_genes(genes):
    """
    Returns the probability of inheritance of the genes
    """
    if genes == 1:
        return .5
    elif genes == 2:
        return (1-PROBS["mutation"])
    else:
        return PROBS["mutation"]


def person_genes(person, one_gene, two_genes):
    """
    Returns the genes of the person in question
    """
    if person in one_gene:
        return 1 
    elif person in two_genes:
        return 2
    return 0

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
    p_world = 1
    for person, data in people.items():
        p = 1
        p_genes = person_genes(person=person, one_gene=one_gene, two_genes=two_genes)
        person_trait = person in have_trait # If has the trait (True or False)

        mother = data['mother']
        father = data['father']
        
        p *= PROBS["trait"][p_genes][person_trait]
        if not mother and not father:
            p *= PROBS["gene"][p_genes]
        else:
            father_genes = person_genes(person=father, one_gene=one_gene, two_genes=two_genes)
            mother_genes = person_genes(person=mother, one_gene=one_gene, two_genes=two_genes)

            father_probability = prob_of_genes(father_genes) # Probability of inheritance
            mother_probability = prob_of_genes(mother_genes) # Probability of inheritance

            if p_genes == 0:
                p *= (1-father_probability) * (1-mother_probability)

            elif p_genes == 1:
                # probability of one or the other:
                p_father_not_mother = (father_probability) * (1 - mother_probability)
                p_mother_not_father = (1 - father_probability) * (mother_probability)
                p *= p_father_not_mother + p_mother_not_father
            else:
                p *= father_probability  * mother_probability
        p_world *= p
    return p_world

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        p_genes = person_genes(person=person, one_gene=one_gene, two_genes=two_genes)
        p_trait = person in have_trait # If has the trait (True or False)
        probabilities[person]['gene'][p_genes] += p
        probabilities[person]['trait'][p_trait] += p


def normalize(probabilities: dict):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person, prob_person in probabilities.items():
        for trait, prob_trait in prob_person.items():
            sum_prob = sum(prob_trait.values())
            for key, value in prob_trait.items():
                probabilities[person][trait][key] /= sum_prob
    return probabilities


if __name__ == "__main__":
    main()