from flask import Flask, request, jsonify
import pandas as pd
import pprint

# Initialiser l'application Flask
app = Flask(__name__)

# Charger les fichiers de données au démarrage de l'application
names_df = pd.read_excel('ESRS_NAMES_EN-FR.xlsx')
acronyms_df = pd.read_excel('ESRS_ACRONYMS_EN-FR.xlsx')
corpus_df = pd.read_excel('CORPUS_ESRS_EN_FR - GIT.xlsx')

pprint.pprint(corpus_df)

# Créer des dictionnaires de traduction
names_dict = dict(zip(names_df['EN'], names_df['FR']))
acronyms_dict = dict(zip(acronyms_df['EN'], acronyms_df['FR']))
corpus_dict = dict(zip(corpus_df['EN'], corpus_df['FR']))

# Fonction de traduction
def preprocess_text(text):
    words = text.split()
    translated_words = [acronyms_dict.get(word, names_dict.get(word, word)) for word in words]
    return " ".join(translated_words)

def translate_sentence(sentence):
    return corpus_dict.get(sentence, preprocess_text(sentence))

# Point de terminaison de traduction
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    sentence = data.get("sentence", "")
    translated_text = translate_sentence(sentence)
    return jsonify({"translated_text": translated_text})

if __name__ == '__main__':
    app.run(debug=True)
