"""String similarity metrics and string utils.

String similarity metrics or string distance functions measure the distance 
between two strings for approximate string matching/comparison. 
"""

import json
from math import sqrt

def extract_ngrams(string, n=3, padding=True):
    """Break a string into a sequence of n adjacent letters or ngrams. 
    Optionally add spaces to mark the the beginning and end of the string."""

    # Add extra-spaces at beginning and end
    if padding:
        string = (n-1) * " " + string + (n-1) * " "

    return [string[i:i+n] for i in range(len(string)-n+1)]


def vectorize_ngrams(ngrams, normalize=True):
    """Count the number of occurences in a list of ngrams. This is similar to 
    constructing a vector (here stored as a dictionary) in the ngram-space."""

    ngrams_vector = {}
    # Count the number of ngrams
    for ngram in ngrams:
        if ngram in ngrams_vector:
            ngrams_vector[ngram] += 1
        else:
            ngrams_vector[ngram] = 1
    # Divide count to get a unit vector
    if normalize:
        norm = sqrt(sum([v**2 for v in ngrams_vector.values()]))
        for ngram in ngrams_vector.keys():
            ngrams_vector[ngram] /= norm

    return ngrams_vector


def cosine_similarity(v_1_json, v_2_json):
    """Measure of similarity (from 0. to 1.) between two strings using the 
    angle between their normalized ngrams vectors (stored as dictionaries)."""

    # Deserialize strings to dicts (cannot store dicts directly in database)
    v_1 = json.loads(v_1_json)
    v_2 = json.loads(v_2_json)
    # Dot product between v_1 and v_2 (unit vectors)
    common_ngrams = set(v_1.keys()) & set(v_2.keys())

    return sum([v_1[ngram] * v_2[ngram] for ngram in common_ngrams])


def is_year(string):
    """Check if a word represents a year."""

    return string.isdigit()

