# app.py
from flask import Flask, render_template, request
import requests, re

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    input_word = ""
    definition = None
    part_of_speech = None
    synonyms = None
    antonyms = None
    pronunciation = None
    examples = None
    etymology = None

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
                definition = get_definition(data, input_word)
            else:
                definition = 'Error fetching definition.'

        # If the user presses the 'Show part of speech' button
        elif action == 'pos':
            response = requests.get(urls['collegiate'])

            if response.status_code == 200:
                data = response.json()
                part_of_speech = show_part_of_speech(data, input_word, part_of_speech)
            else:
                part_of_speech = 'Error fetching the parts of speech.'

        # If the user presses the 'Get synonyms' button
        elif action == 'synonyms':
            response = requests.get(urls['thesaurus'])

            if response.status_code == 200:
                data = response.json()
                synonyms = get_synonyms(data, input_word)
            else:
                synonyms = 'Error fetching synonyms.'

        # If the user presses the 'Get antonyms' button
        elif action == 'antonyms':
            response = requests.get(urls['thesaurus'])

            if response.status_code == 200:
                data = response.json()
                antonyms = get_antonyms(data, input_word)
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
                examples = provide_examples(data, input_word)
            else:
                examples = 'Error fetching examples.'

        # If the user the presses the 'Show etymology' button
        elif action == 'etymology':
            response = requests.get(urls['collegiate'])

            if response.status_code == 200:
                data = response.json()
                etymology = show_etymology(data)
            else:
                etymology = 'Error fetching etymology.'

    return render_template('dictionary_app.html',
                           input_word=input_word,
                           definition=definition, pos=part_of_speech, synonyms=synonyms, antonyms=antonyms,
                           pronunciation=pronunciation, examples=examples, etymology=etymology)


def get_definition(data,  input_word):
    definitions = data[0].get('shortdef', [f'No definition for the word {input_word}.'])
    definition = ''
    if definitions:
        for i, defn in enumerate(definitions, 1):
            # Append each definition to the 'definition' string
            definition += f"{i}. {defn}<br>"
    else:
        definition = 'No definition found.'
    return definition


def show_part_of_speech(data, input_word, part_of_speech):
    pos = data[0].get('fl', [f'The word {input_word} does not belong to any part of speech.'])
    part_of_speech = pos
    return part_of_speech


def get_synonyms(data, input_word):
    synonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('syn_list',
                                                           [f'No synonyms for the word {input_word} found.'])
    synonyms = ''
    if synonyms_list:
        for i, syn in enumerate(synonyms_list[0], 1):
            synonyms += f"{i}. {syn['wd']}<br>"
    else:
        synonyms = 'No synonyms found.'
    return synonyms


def get_antonyms(data, input_word):
    antonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('ant_list',
                                                           [f'No antonyms for the word {input_word} found.'])
    antonyms = ''
    if antonyms_list:
        for i, ant in enumerate(antonyms_list[0], 1):
            antonyms += f"{i}. {ant['wd']}<br>"
    else:
        antonyms = 'No antonyms found.'
    return antonyms


def get_pronunciation(data, input_word, pronunciation):
    pronunciation = data[0]['hwi']['prs'][0].get('mw',
                                                 f'No pronunciations for the word {input_word} were found.')
    return pronunciation


def provide_examples(data, input_word):
    quotes = data[0].get('quotes', [f'No examples for the word {input_word} were found.'])
    examples = ''
    if quotes:
        for i, quote in enumerate(quotes, 1):
            if 't' in quote:
                cleaned_t_value = quote['t'].replace("{qword}", "").replace("{/qword}", "")
                examples += f"{i}. {cleaned_t_value}<br>"
            else:
                examples = 'No examples found.'
    else:
        examples = 'No examples found.'
    return examples


def show_etymology(data):
    et = data[0]['et'][0][1]

    etymology = ()
    if et:
        cleaned_etymology = ''.join(et).replace("{it}", "").replace("{/it}", "") # clean the tags

        # Split by both comma and semicolon in one line using re.split
        etymology_parts = re.split(r', |; ', cleaned_etymology)
        et_entry = ""
        print("Etymology:")
        for i, part in enumerate(etymology_parts, 1):
            # Print each part on a new line with numbering
            et_entry += f"{i}. {part}<br>"

    date_entry = data[0]['date']
    cleaned_date = re.sub(r'\{[^}]*\}', '', date_entry)

    etymology = (et_entry, cleaned_date)
    return etymology


if __name__ == '__main__':
    app.run(debug=True, port=5003)
