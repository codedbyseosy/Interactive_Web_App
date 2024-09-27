# app.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    input_word = None
    definition = None
    synonyms = None
    antonyms = None
    pronunciation = None
    examples = None

    api_keys = [
        "47a18b32-61c5-4951-ad64-1fdbbf295a5d",
        "864ede40-eae9-41c8-98c3-c24c92e8dd4e"
    ]



    if request.method == 'POST':
        input_word = request.form['input_word']
        action = request.form['action']  # Check which button has been pressed

        urls = {
            "thesaurus": f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{input_word}?key={api_keys[0]}",
            "collegiate": f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{input_word}?key={api_keys[1]}"
        }

        # If the user presses the 'Get definition' button
        if action == 'definition':
            response = requests.get(urls['thesaurus'])

            if response.status_code == 200:
                data = response.json()
                definition = get_definition(data, definition, input_word)
            else:
                definition = 'Error fetching definition.'

        # If the user presses the 'Get synonyms' button
        elif action == 'synonyms':
            response = requests.get(urls['thesaurus'])

            if response.status_code == 200:
                data = response.json()
                synonyms = get_synonyms(data, input_word, synonyms)
            else:
                synonyms = 'Error fetching synonyms.'

        # If the user presses the 'Get synonyms' button
        elif action == 'antonyms':
            response = requests.get(urls['thesaurus'])

            if response.status_code == 200:
                data = response.json()
                antonyms = get_antonyms(antonyms, data, input_word)
            else:
                antonyms = 'Error fetching antonyms.'

        # If the user presses the 'Get pronunciation' button
        elif action == 'pronunciation':
            response = requests.get(urls['collegiate'])

            if response.status_code == 200:
                data = response.json()
                pronunciation = get_pronunciation(data, input_word, pronunciation)
            else:
                pronunciation = 'Error fetching pronunciations.'

        # If the user the presses the 'Provide examples' button
        elif action == 'examples':
            response = requests.get(urls['collegiate'])

            if response.status_code == 200:
                data = response.json()
                examples = provide_examples(data, examples, input_word)
            else:
                examples = 'Error fetching examples.'

    return render_template('dictionary_app.html',
                           input_word=input_word,
                           definition=definition, synonyms=synonyms, antonyms=antonyms,
                           pronunciation=pronunciation, examples=examples)


def get_definition(data, definition, input_word):
    definitions = data[0].get('shortdef', [f'No definition for the word {input_word}.'])
    if definitions:
        definition = '\n'.join(f"{i + 1}. {defn}" for i, defn in enumerate(definitions))
    else:
        definition = 'No definition found.'
    return definition


def get_synonyms(data, input_word, synonyms):
    synonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('syn_list',
                                                           [f'No synonyms for the word {input_word} found.'])
    if synonyms_list:
        for i, syn in enumerate(synonyms_list[0]):
            synonyms = '\n'.join(f"{i + 1}. {syn['wd']}")
    else:
        synonyms = 'No synonyms found.'
    return synonyms


def get_antonyms(antonyms, data, input_word):
    antonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('ant_list',
                                                           [f'No antonyms for the word {input_word} found.'])
    if antonyms_list:
        for i, ant in enumerate(antonyms_list[0]):
            antonyms = '\n'.join(f"{i + 1}. {ant['wd']}")
    else:
        antonyms = 'No antonyms found.'
    return antonyms


def get_pronunciation(data, input_word, pronunciation):
    pronunciation = data[0]['hwi']['prs'][0].get('mw',
                                                 f'No pronunciations for the word {input_word} were found.')
    return pronunciation


def provide_examples(data, examples, input_word):
    quotes = data[0].get('quotes', [f'No examples for the word {input_word} were found.'])
    if quotes:
        for i, quote in enumerate(quotes):
            if 't' in quote:
                examples = '\n'.join(f"{i + 1}. {quote['t']}")
            else:
                examples = 'No examples found.'
    else:
        examples = 'No examples found.'
    return examples


if __name__ == '__main__':
    app.run(debug=True, port=5001)
