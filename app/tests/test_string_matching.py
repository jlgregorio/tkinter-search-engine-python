import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest

from string_utils import extract_ngrams, vectorize_ngrams, cosine_similarity


class TestStringMatching(unittest.TestCase):

    def test_unigrams_extraction(self):

        # A pangram is a sentence that contains all the letters of the alphabet
        pangram = "The quick brown fox jumps over the lazy dog"
        unigrams = extract_ngrams(pangram, 1, False)
        alphabet_letters = "abcdefghijklmnopqrstuvwxyz"
        self.assertTrue(all([letter in unigrams for letter in alphabet_letters]))

    def test_cosine_similarity_same(self):

        ngrams = extract_ngrams("The quick brown fox jumps over the lazy dog")
        vector = vectorize_ngrams(ngrams)
        score = cosine_similarity(vector, vector)
        self.assertEqual(score, 1.0)

    def test_cosine_similarity_none(self):
        
        ngrams_1 = extract_ngrams("The quick brown fox jumps over the lazy dog", 4, False)        
        ngrams_2 = extract_ngrams("Sphinx of black quartz, judge my vow", 4, False)
        vector_1 = vectorize_ngrams(ngrams_1)
        vector_2 = vectorize_ngrams(ngrams_2)
        score = cosine_similarity(vector_1, vector_2)
        self.assertEqual(score, 0.0)

    def test_cosine_similarity_half(self):
        
        ngrams_1 = extract_ngrams("abcdxx", 3, False)        
        ngrams_2 = extract_ngrams("abcdyy", 3, False)
        vector_1 = vectorize_ngrams(ngrams_1)
        vector_2 = vectorize_ngrams(ngrams_2)
        score = cosine_similarity(vector_1, vector_2)
        self.assertEqual(score, 0.5)


if __name__=="__main__":

    unittest.main()
