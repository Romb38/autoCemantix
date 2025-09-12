Beam Solving
============

*Average solving time* : 400 seconds (~ 7min)

*Worst case solving time* : 10200 seconds (~ 3hours)

I've used this method when I had a model that did not produce the same scores as Cemantix.

This solving method works as follows:

1. I request the score for 5 starting words and sort them in decreasing order.
2. I take the first word from the stack (the one with the highest score found) and use the model to find the 20 nearest untested words.
3. For each of these 20 words, I request their scores and add them to the stack, again sorted by decreasing score.
4. Repeat steps 2 and 3 until a word with a score of **1.0** is found.

If no word with a score of **1.0** is found, it means that the target word is not present in the model.

This method has a high likelihood of fast convergence because at each step, we explore the most promising candidates first.
It also guarantees eventual convergence, as we systematically check every word in the model.
