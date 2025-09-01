<h1 align="center">Cemantix Auto-Solver</h1>
<p align="center">
  <img src="https://img.shields.io/github/last-commit/Romb38/autoCemantix?style=flat-square" />
</p>


This project aims to solve automatically [Cemantix puzzle](https://cemantix.certitudes.org/). It also let the user filter his model to adapt his own dictionary

## Installation

```bash
# On project root

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Execution of the solver

```bash
source .venv/bin/activate
python3 main.py solve
```

## Configuration

You can configure this script using the config file located at `src/ressources/config.ini`

## Dictionnary filtering

It is currently in WIP stage but you can use `basic_filtering.py` to filter the standard dictionary to limit computing time. It applies the following filters :
- Word exists in French Dictionnary
- Word have more than 1 letters
- Word is not a conjugated verb
- Word is not plural
- Word do not start by non-alphanumeric characters
- Word do not contains non-alphanumeric characters other than "-"

## Start the filtering

With the `frWac.bin` in `src/ressources` folder

```bash
python3 src/basic_filtering.py
```

## Ressources
This project use the following ressources :

French dictionnary : http://www.lexique.org/
Cemantix dictionnary : https://fauconnier.github.io/#data
