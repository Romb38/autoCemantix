Solving Methods
===============

*Average solving time* : 0.5 seconds (with filtered model)

In this project, I've implemented several methods to solve **Cemantix**. Here's how the current approach works:

1. I request the score for a set of starting words (defined in the configuration file) using parallelization.
2. Using **NumPy**, I compute the `cosine similarity <https://en.wikipedia.org/wiki/Cosine_similarity>`_ between every word and the starting words.
3. I then filter and save the words whose cosine similarity is approximately equal to the score of the starting words (within a small epsilon).
4. For each word identified in step 3, I request its Cemantix score:

   - If the score is **1.0**, the solution has been found and the process stops.
   - If not, the process continues with the next candidate.

If no word reaches a score of **1.0**, it means the target word is likely not present in my model, and I cannot solve the daily Cemantix puzzle.

.. toctree::
   :maxdepth: 1
   :caption: Old solving methods

   old_methods/beam_solving
   old_methods/local_score
