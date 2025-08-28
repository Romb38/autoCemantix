# Cemantix solver

This project aims to solve automatically [Cemantix puzzle](https://cemantix.certitudes.org/).

## Installation

Firstly, go to [Jean-Philippe Fauconnier's page](https://fauconnier.github.io/#data) and download `bin (120Mb) - cbow` in `frWac2Vec`, name it `frWac.bin` and place it in `src/ressources/`.

Then,
```bash
# On project root

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Execution

```bash
source .venv/bin/activate
python3 main.py
```

## Configuration

You can configure this script using the config file located at `src/ressources/config.ini`


## Dictionnary

For this project, I used the dictionnary available on [Jean-Philippe Fauconnier's page](https://fauconnier.github.io/#data)
