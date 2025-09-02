<h2 align="center">Cemantix Auto-Solver</h2>
<p align="center">
  <img src="https://img.shields.io/github/last-commit/Romb38/autoCemantix?style=flat-square" />
  <a href="https://github.com/Romb38/autoCemantix/blob/master/TODO.md">
    <img src="https://img.shields.io/badge/Roadmap-View-blue?style=flat-square" alt="Roadmap" />
  </a>
</p>

This project aims to automatically solve the [Cemantix puzzle](https://cemantix.certitudes.org/) as quickly and efficiently as possible. It also let the user filter his model to fit it own dictionary.

## 🛠️ Installation

```bash
# On project root

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## 🚀 Solver execution

Without configuration, the solver use default dictionary, filtered by `initialFiltering.py`

```bash
source .venv/bin/activate
python3 main.py solve
```

## 🧹 Dictionary filtering

To start filtering a new Word2Vec model, follow these steps :
- Change the `model_path` properties in the [configuration file](#-configuration) to point to your new model
- Execute the following, it will take a bit of time, but you can follow the filtering inside of logs (default location : `logs/solver.log`)
```bash
source .venv/bin/activate
python3 main.py init &
```

To give you more information, this script applies the following filters :
- Word exists in French dictionary
- Word have more than 1 letters
- Word is not a conjugated verb
- Word is not plural
- Word do not start by non-alphanumeric characters
- Word do not contains non-alphanumeric characters other than "-"
- Word is not inside of previously tested word (listed in `src/resources/invalid_words.pkl`)

To applies these filter, the script is using this [glossary](http://www.lexique.org/).

## 📊 Statistics

Everyday, the first solving is saved in a file `src/resources/stats.csv`. It is only saved if the word is found. Currently, we save the following :

```
timestamp, -> When statistics ar saved
puzzle_number, -> Puzzle number (given by Cemantix)
word, -> Answer of the Cemantix puzzle
solving_time, -> Solving time
requests_count, -> Number of requests used to solve the puzzle
api_delay, -> Delay between each solve (as set in configuration file)
invalid_word_removed_count -> Number of invalid word found during the solving
```

We save only the first solving because we remove invalid_words from the model. This fact let statistics becomes false after 1 solving.

## 🔧 Configuration

Configuration file location : `src/resources/config.ini`

You can configure a lot this script, but it is advised to use the default configuration.

## 🔔 Ntfy Configuration

In this project, i used [ntfy](https://ntfy.sh/) to send me custom notification with some statistics. Here is the line that I'm using to send the notification :

```bash
ntfy publish --token {token} {ntfy_url}/{subject} "{msg}"
```

Values in brackets are configured by using a `.env` file located at the root of the project. You can use the `.env.example`

```bash
NTFY_TOKEN=XXXXX # Token is required if you're using a instance with password
NTFY_SUBJECT=XXXXX # Subject to send notification to
NTFY_URL=https://ntfy.exemple.fr # Adress of the ntfy server
```

## 📚 Resources
This project use the following resources :

- French glossary : http://www.lexique.org/

The french glossary is used when you want to filter your own model. It is used to know if a word is plural or conjugated.

- Cemantix dictionary (from Jean-Philippe Fauconnier): https://fauconnier.github.io/#data

I've used [this model](https://embeddings.net/embeddings/frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin) (bin (120Mb) cbow) with my filtering script to get the current `src/resources/frWac.bin` file. This file is also filtered everyday by removing all invalid words found when the script is running.
