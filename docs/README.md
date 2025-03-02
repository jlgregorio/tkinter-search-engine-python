## About approximate string matching

One feature of this "Search Engine" is the ability to provide a list of results even if the user's input does not perfectly match an entry of the database. This is made possible by using an approximate string matching or fuzzy search algorithm, which simply measures "how close two strings are".

There are in practice many string matching algorithms (including the well-known *Leveinstein distance*). The one implemented here is fairly simple and fast, and offers relatively good performance. It works as described below:

1. Strings are broken into small chunks of $n$ consecutive letters, also called *n-grams*. The number $n$ is arbitrarily set to 3 here, giving a set of *trigrams* for each string.

2. Vectors are constructed from these trigrams by counting how often they appear for a given string.

3. The angles between vectors are used to measure similarity between strings. With $v_1$ and $v_2$ being two vectors, it is simply $cos \theta = (v_1 \cdot v_2)/(||v_1|| . ||v_2||)$. The  *cosine similarity* ranges from 1 (collinear vectors) to 0 (orthogonal vectors).

For example, "Paris" contains the trigrams "Par", "ari", and "ris" while "Rome" contains the trigrams "Rom" and "ome". Arranging trigrams in the order ("Par", "ari", "ris", "Rom", "ome") allow us to write the words "Paris" and "Rome" as vectors such as $v_1 = [1, 1, 1, 0, 0]$ and $v_2 = [0, 0, 0, 1, 1]$. It simply means that the word "Paris" contains the trigrams "Par", "ari", and "ris" once (and does not contain the trigrams "Rom" and "ome"). $v_1$ and $v_2$ being orthogonal here, the *cosine similarity* is equal to 0 and we can conclude that the words "Paris" and "Rome" are completely dissimilar.

While this algorithm is already quite simple and efficient, a few tricks are added to ease and speed up calculations:
* Vectors are computed and stored for all entries of the database.
* Vectors are stored as dictionaries/JSON strings instead of real vectors made out of all possible trigrams ("aaa", "aab", "aac", etc.).
* Stored vectors are normalized so that the computation of $||v_i||$ is not necessary.

This makes the comparison of an input string with thousands of database entries possible in less than a second.
