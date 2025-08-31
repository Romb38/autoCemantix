import pandas as pd
from gensim.models import KeyedVectors
import re

# Charger le fichier TSV avec pandas
file_path = 'ressources/Lexique383.tsv'  # Remplace par le chemin vers ton fichier
df = pd.read_csv(file_path, sep='\t')
model = KeyedVectors.load_word2vec_format("ressources/frWac.bin", binary=True, unicode_errors="ignore")

def is_valid_word(word):
    if len(word) < 2:
        return False

    # Vérifier si le mot commence par un caractère alphanumérique
    if not word[0].isalnum():
        return False
    
    # Vérifier si le mot contient des caractères non alphanumériques sauf "-"
    if not re.match(r'^[a-zA-Z0-9-]*$', word):
        return False

    return True

# Fonction pour vérifier si un mot est au pluriel
def is_plural(word):
    word_data = df[df['ortho'] == word]
    if not word_data.empty:
        return word_data.iloc[0]['nombre'] == 'p'
    return False

# Fonction pour vérifier si un mot est une forme conjuguée
def is_conjugated(word):
    word_data = df[df['ortho'] == word]
    if not word_data.empty:
        # Un mot est conjugué s'il est un verbe ou un auxiliaire
        cgram = word_data.iloc[0]['cgram']
        if type(cgram) != float:
            return 'VER' in cgram or 'AUX' in cgram
    return False

def exists(word):
    word_data = df[df['ortho'] == word]
    if not word_data.empty:
        return True
    return False

def filter_words(model):
    filtered_words = {}
    total_words = len(model.key_to_index)  # Nombre total de mots dans le modèle
    processed_words = 0  # Compteur des mots traités

    for word in model.key_to_index.keys():
        processed_words += 1

        # Affichage du pourcentage de progression
        if processed_words % (total_words // 100) == 0:  # Affiche chaque 1% de progression
            percent = (processed_words / total_words) * 100
            print(f"Progression : {percent:.2f}% ({processed_words}/{total_words} mots traités)")

        # Filtrage des mots
        if not(exists(word)) or not(is_valid_word(word)) or is_plural(word) or is_conjugated(word):
            continue  # Si le mot est pluriel ou conjugué, on l'ignore
        
        filtered_words[word] = model[word]
    
    return filtered_words

# Appliquer le filtrage des mots
filtered_words = filter_words(model)

# Créer un nouveau modèle Word2Vec avec les mots filtrés
filtered_model = KeyedVectors(vector_size=model.vector_size)

# Ajouter les vecteurs des mots filtrés dans le nouveau modèle
filtered_model.add_vectors(list(filtered_words.keys()), list(filtered_words.values()))

# Sauvegarder le modèle filtré dans un fichier
filtered_model.save_word2vec_format("ressources/filtered_frWac.bin", binary=True)
print("Le modèle filtré a été sauvegardé sous 'filtered_frWac.bin'")

