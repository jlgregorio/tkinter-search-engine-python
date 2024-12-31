"""String similarity metrics and string utils.

String similarity metrics or string distance functions measure the distance 
between two strings for approximate string matching/comparison. 
"""

from math import sqrt

def extract_ngrams(string, n=3, padding=True):
    """Break a string into a sequence of n adjacent letters."""

    # Add extra-spaces at start and end
    if padding:
        string = (n-1) * " " + string + (n-1) * " "

    return [string[i:i+n] for i in range(len(string)-n+1)]


def vectorize_ngrams(ngrams, normalize=True):
    """Transform ngrams into sparse (DoK) vector."""

    ngrams_vector = {}
    # Count occurences of each ngram
    for ngram in ngrams:
        if ngram in ngrams_vector:
            ngrams_vector[ngram] += 1
        else:
            ngrams_vector[ngram] = 1
    # Normalize
    if normalize:
        norm = sqrt(sum([v**2 for v in ngrams_vector.values()]))
        for ngram in ngrams_vector.keys():
            ngrams_vector[ngram] /= norm

    return ngrams_vector


def cosine_similarity(ngrams_v_1, ngrams_v_2):
    """Measure of similarity between normalized ngrams vectors."""

    common_ngrams = set(ngrams_v_1.keys()) & set(ngrams_v_2.keys())

    return sum([ngrams_v_1[ngram] * ngrams_v_2[ngram] for ngram in common_ngrams])

