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
            try:
                response = requests.get(urls['thesaurus'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    definition = get_definition(data, input_word)
                else:
                    definition = 'Error fetching definition.'
            except TypeError:
                print(f"Oops! We received unexpected data from the dictionary service. "
                      "Please try again later or check the word you're looking up.")
            except requests.exceptions.Timeout:
                print("It looks like the request took too long. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.ConnectionError:
                print("We're having trouble connecting to the dictionary service. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}. Please try again later.")

        # If the user presses the 'Show part of speech' button
        elif action == 'pos':
            try:
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    part_of_speech = show_part_of_speech(data, input_word, part_of_speech)
                else:
                    part_of_speech = 'Error fetching the parts of speech.'

            except TypeError:
                print(f"Oops! We received unexpected data from the dictionary service. "
                      "Please try again later or check the word you're looking up.")
            except requests.exceptions.Timeout:
                print("It looks like the request took too long. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.ConnectionError:
                print("We're having trouble connecting to the dictionary service. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}. Please try again later.")

        # If the user presses the 'Get synonyms' button
        elif action == 'synonyms':
            try:
                response = requests.get(urls['thesaurus'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    synonyms = get_synonyms(data, input_word)
                else:
                    synonyms = 'Error fetching synonyms.'

            except TypeError:
                print(f"Oops! We received unexpected data from the dictionary service. "
                      "Please try again later or check the word you're looking up.")
            except requests.exceptions.Timeout:
                print("It looks like the request took too long. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.ConnectionError:
                print("We're having trouble connecting to the dictionary service. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}. Please try again later.")

        # If the user presses the 'Get antonyms' button
        elif action == 'antonyms':
            try:
                response = requests.get(urls['thesaurus'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    antonyms = get_antonyms(data, input_word)
                else:
                    antonyms = 'Error fetching antonyms.'

            except TypeError:
                print(f"Oops! We received unexpected data from the dictionary service. "
                      "Please try again later or check the word you're looking up.")
            except requests.exceptions.Timeout:
                print("It looks like the request took too long. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.ConnectionError:
                print("We're having trouble connecting to the dictionary service. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}. Please try again later.")

        # If the user presses the 'Get pronunciation' button
        elif action == 'pronunciation':
            try:
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    pronunciation = get_pronunciation(data, input_word, pronunciation)
                else:
                    pronunciation = 'Error fetching pronunciations.'

            except TypeError:
                print(f"Oops! We received unexpected data from the dictionary service. "
                      "Please try again later or check the word you're looking up.")
            except requests.exceptions.Timeout:
                print("It looks like the request took too long. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.ConnectionError:
                print("We're having trouble connecting to the dictionary service. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}. Please try again later.")

        # If the user the presses the 'Provide examples' button
        elif action == 'examples':
            try:
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    examples = provide_examples(data, input_word)
                else:
                    examples = 'Error fetching examples.'

            except TypeError:
                print(f"Oops! We received unexpected data from the dictionary service. "
                      "Please try again later or check the word you're looking up.")
            except requests.exceptions.Timeout:
                print("It looks like the request took too long. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.ConnectionError:
                print("We're having trouble connecting to the dictionary service. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}. Please try again later.")

        # If the user the presses the 'Show etymology' button
        elif action == 'etymology':
            try:
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    etymology = show_etymology(data)
                else:
                    etymology = 'Error fetching etymology.'

            except TypeError:
                print(f"Oops! We received unexpected data from the dictionary service. "
                      "Please try again later or check the word you're looking up.")
            except requests.exceptions.Timeout:
                print(
                    "It looks like the request took too long. "
                    "Please check your internet connection and try again later.")

            except requests.exceptions.ConnectionError:
                print("We're having trouble connecting to the dictionary service. "
                      "Please check your internet connection and try again later.")

            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred: {e}. Please try again later.")

    return render_template('dictionary_app.html',
                           input_word=input_word,
                           definition=definition, pos=part_of_speech, synonyms=synonyms, antonyms=antonyms,
                           pronunciation=pronunciation, examples=examples, etymology=etymology)


def get_definition(data, input_word):
    try:
        definitions = data[0].get('shortdef', [f'No definition for the word {input_word}.'])
        definition = ''
        for i, defn in enumerate(definitions, 1):
            # Append each definition to the 'definition' string
            definition += f"{i}. {defn}<br>"

    except (IndexError, KeyError):
        # Handle the case where 'shortdef' is missing
        definition = f"Sorry, no definitions for the word '{input_word}' were found."

    return definition


def show_part_of_speech(data, input_word):
    try:
        pos = data[0].get('fl', [f'The word {input_word} does not belong to any part of speech.'])
        part_of_speech = pos

    except (IndexError, KeyError):
        # Handle the case where 'fl' is missing
        part_of_speech = f"Sorry, we couldn't find what part of speech the word '{input_word}' belongs to."

    return part_of_speech


def get_synonyms(data, input_word):
    try:
        synonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('syn_list',
                                                               [f'No synonyms for the word {input_word} found.'])
        synonyms = ''
        for i, syn in enumerate(synonyms_list[0], 1):
            synonyms += f"{i}. {syn['wd']}<br>"

    except (IndexError, KeyError):
        # Handle the case where 'syn_list' is missing
        synonyms = f"Sorry, we couldn't find any synonyms for the word '{input_word}'."

    return synonyms


def get_antonyms(data, input_word):
    try:
        antonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('ant_list',
                                                               [f'No antonyms for the word {input_word} found.'])
        antonyms = ''
        for i, ant in enumerate(antonyms_list[0], 1):
            antonyms += f"{i}. {ant['wd']}<br>"

    except (IndexError< KeyError):
        # Handle the case where 'ant_list' is missing
        antonyms = f"Sorry, we couldn't find any antonyms for the word '{input_word}'."

    return antonyms


def get_pronunciation(data, input_word):
    try:
        pronunciation = data[0]['hwi']['prs'][0].get('mw', f"No pronunciations for the word '{input_word}' were found.")
    except (IndexError, KeyError):
        # Handle the case where 'mw' is missing
        pronunciation = f"Sorry, we couldn't find any pronunciations for the word '{input_word}'."
    return pronunciation


def provide_examples(data, input_word):
    quotes = data[0].get('quotes', [f'No examples for the word {input_word} were found.'])
    examples = ''
    try:
        for i, quote in enumerate(quotes, 1):
            if 't' in quote:
                cleaned_t_value = quote['t'].replace("{qword}", "").replace("{/qword}", "")
                examples += f"{i}. {cleaned_t_value}<br>"
            else:
                examples = 'No examples found.'

    except (IndexError, KeyError):
        # Handle the case where 'quotes' or 't' key is missing
        examples = f"Sorry, we couldn't find any examples for how to use the word '{input_word}'."

    return examples


def show_etymology(data):
    et = data[0]['et'][0][1]

    etymology = ()
    try:
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

    except (IndexError, KeyError):
        # Handle the case where 'et' or 'date' keys are missing
        print(f"Sorry, the etymology data for the word '{input_word}' does not exist")

    return etymology


if __name__ == '__main__':
    app.run(debug=True, port=5003)
