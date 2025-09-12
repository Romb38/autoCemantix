<h1 align="center">Cemantix Auto-Solver</h1>
<p align="center">
  <img src="https://img.shields.io/github/last-commit/Romb38/autoCemantix?style=flat-square" />
  <a href="https://github.com/Romb38/autoCemantix/blob/master/TODO.md">
    <img src="https://img.shields.io/badge/Roadmap-View-blue?style=flat-square" alt="Roadmap" />
  </a>
  <a href="https://github.com/Romb38/autoCemantix/actions/workflows/build-docs.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/Romb38/autoCemantix/build-docs.yml?style=flat-square" alt="Documentation build" />
  </a>
</p>

This project aims to automatically solve the [Cemantix puzzle](https://cemantix.certitudes.org/) as quickly and efficiently as possible.

## 📂 Fetching project

This project use `git-lfs` to store the model inside of the repository. You'll need to install it if you want to pull the right model. On Debian based computer :

```bash
# Installation
sudo apt install git-lfs
git lfs install

# Fetching the model
git lfs pull
```

You can also download it by yourself :

```bash
# On project root

curl https://github.com/Romb38/autoCemantix/raw/refs/heads/master/src/resources/frWac.bin -o src/resources/frWac.bin
```


## 🛠️ Installation

```bash
# On project root

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## 🚀 Solver execution

Without configuration, the solver use default dictionary, same as Cemantix dictionary.

```bash
source .venv/bin/activate
python3 main.py solve
```

You can also add options to this script :
```
--ntfy/-n : Enable notification using NTFY services. A configuration must be made inside of .env (c.f README.md - Ntfy Configuration)
```

## 🔧 Configuration

Configuration file location : `src/resources/config.ini`

You can configure a lot this script, but it is advised to use the default configuration.

## 🔔 Ntfy Configuration

In this project, i used a [ntfy](https://ntfy.sh/) server to send me custom notification with some statistics. Here is the line that I'm using to send the notification :

```bash
curl -H "Authorization: Bearer {token}" -d "{msg}" {ntfy_url}/{subject}
```

Values in brackets are configured by using a `.env` file located at the root of the project. You can see them `.env.example`

```bash
NTFY_TOKEN=XXXXX # Token is required if you're using a instance with password
NTFY_SUBJECT=XXXXX # Subject to send notification to
NTFY_URL=https://ntfy.exemple.fr # Adress of the ntfy server
```

## 📚 Resources
This project use the following resources :

- Cemantix dictionary (from Jean-Philippe Fauconnier): https://fauconnier.github.io/#data

I've used [this model](https://embeddings.net/embeddings/frWac_no_postag_phrase_500_cbow_cut10.bin) (bin (2Gb) cbow 500 10 14da). It has been filtered to be the same as Cemantix dictionary.
