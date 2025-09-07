Resources folder
================

In this section, we describe each file you can find in the ``src/resources/`` folder.

``config.ini``
--------------

This file contains the project configuration. It includes many project variables and is self-documented.

``frWac.bin``
-------------

This is the base model, obtained from `Jean-Philippe Fauconnier's page <https://fauconnier.github.io/#data>`_ and filtered locally. It is used by default to compute statistics, such as the average number of invalid words found during each round of solving Cemantix.

``frWac_filtered.bin``
----------------------

This is the same model as above, but with every word checked using the Cemantix API. With this model, you're guaranteed to get only valid words — but not necessarily *all* the words known by Cemantix.

``invalid_words.pkl``
---------------------

A `Pickle binary <https://docs.python.org/3/library/pickle.html>`_ file containing a list of invalid words found during Cemantix solving.

``invalid_words_filtered.pkl``
------------------------------

A `Pickle binary <https://docs.python.org/3/library/pickle.html>`_ file containing a list of invalid words found while checking the model against the Cemantix API.

``Lexique383.tsv``
------------------

A lexicon file from `lexique.org <https://www.lexique.org/>`_, used to locally filter a dictionary.

``stats.csv``
-------------

Statistics collected during each round of Cemantix solving.
