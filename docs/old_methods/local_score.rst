Local Score Solving
====================

*Average solving time* : 5 seconds (with non-filtered model)

*Average solving time* : 2 seconds (with filtered model)

This method relies on having a model that produces the same scores as Cemantix.

1. I request the scores for 3 starting words directly from Cemantix.
2. I compute the similarity between every word in my model and the starting words locally.
   Since we're using the `gensim` and `numpy` libraries, this is much faster than querying Cemantix.

   - If I find a word with the same similarity as the starting words' score, I test it on Cemantix.
     If it has a score of **1.0**, the solution is found and I stop.
   - Otherwise, I continue the search.

If no matching word is found, it likely means that the target word is not present in the model.
