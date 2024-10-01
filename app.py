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
    error_message = None  # To hold any error messages


    api_keys = [
        "47a18b32-61c5-4951-ad64-1fdbbf295a5d",
        "864ede40-eae9-41c8-98c3-c24c92e8dd4e"
    ]

    if request.method == 'POST':

        input_word = request.form['input_word']

        # Input validation: Ensure the input is alphabetic
        if not input_word.isalpha():
            error_message = ("Oops! It looks like you have entered an invalid word."
                             " Please re-enter the word using only alphabetic characters.")
            return render_template('dictionary_app.html', error_message=error_message)

        action = request.form['action']  # Check which button has been pressed

        urls = {
            "thesaurus": f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{input_word}?key={api_keys[0]}",
            "collegiate": f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{input_word}?key={api_keys[1]}"
        }

        try:
            # If the user presses the 'Get definition' button
            if action == 'definition':
                response = requests.get(urls['thesaurus'], timeout=200)
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    definition = get_definition(data, input_word)
                else:
                    error_message = 'Error fetching definition.'

            # If the user presses the 'Show part of speech' button
            elif action == 'pos':
                response = requests.get(urls['collegiate'], timeout=200)
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    part_of_speech = show_part_of_speech(data, input_word)
                else:
                    error_message = 'Error fetching the parts of speech.'

            # If the user presses the 'Get synonyms' button
            elif action == 'synonyms':
                response = requests.get(urls['thesaurus'], timeout=200)
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    synonyms = get_synonyms(data, input_word)
                else:
                    error_message = 'Error fetching synonyms.'

            # If the user presses the 'Get antonyms' button
            elif action == 'antonyms':
                response = requests.get(urls['thesaurus'], timeout=200)
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    antonyms = get_antonyms(data, input_word)
                else:
                    error_message = 'Error fetching antonyms.'

            # If the user presses the 'Get pronunciation' button
            elif action == 'pronunciation':
                response = requests.get(urls['collegiate'], timeout=200)
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    pronunciation = get_pronunciation(data, input_word)
                else:
                    error_message = 'Error fetching pronunciations.'

            # If the user the presses the 'Provide examples' button
            elif action == 'examples':
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    examples = provide_examples(data, input_word)
                else:
                    error_message = 'Error fetching examples.'

            # If the user the presses the 'Show etymology' button
            elif action == 'etymology':
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError as e:
                        print("Invalid JSON format received from the API.")
                        return

                    etymology = show_etymology(data)
                else:
                    error_message = 'Error fetching etymology.'

        except TypeError:
            error_message = "Oops! We received unexpected data from the dictionary service. Please try again later or check the word you're looking up."

        except requests.exceptions.Timeout:
            error_message = "It looks like the request took too long. Please check your internet connection and try again later. "

        except requests.exceptions.ConnectionError:
            error_message = "We're having trouble connecting to the dictionary service. Please check your internet connection and try again later."

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
        error_message = f"Sorry, no definitions for the word '{input_word}' were found."

    except Exception as e:
        error_message = f"An error occurred while fetching the definition: {str(e)}."

    return definition, error_message


def show_part_of_speech(data, input_word):
    try:
        pos = data[0].get('fl', [f'The word {input_word} does not belong to any part of speech.'])
        part_of_speech = pos

    except (IndexError, KeyError):
        # Handle the case where 'fl' is missing
        error_message = f"Sorry, we couldn't find what part of speech the word '{input_word}' belongs to."

    except Exception as e:
        error_message = f"An error occurred while fetching the part of speech: {str(e)}."

    return part_of_speech, error_message


def get_synonyms(data, input_word):
    try:
        synonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('syn_list',
                                                               [f'No synonyms for the word {input_word} found.'])
        synonyms = ''
        for i, syn in enumerate(synonyms_list[0], 1):
            synonyms += f"{i}. {syn['wd']}<br>"

    except (IndexError, KeyError):
        # Handle the case where 'syn_list' is missing
        error_message = f"Sorry, we couldn't find any synonyms for the word '{input_word}'."

    except Exception as e:
        error_message = f"An error occurred while fetching the synonyms: {str(e)}."

    return synonyms, error_message


def get_antonyms(data, input_word):
    try:
        antonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('ant_list',
                                                               [f'No antonyms for the word {input_word} found.'])
        antonyms = ''
        for i, ant in enumerate(antonyms_list[0], 1):
            antonyms += f"{i}. {ant['wd']}<br>"

    except (IndexError< KeyError):
        # Handle the case where 'ant_list' is missing
        error_message = f"Sorry, we couldn't find any antonyms for the word '{input_word}'."

    except Exception as e:
        error_message = f"An error occurred while fetching the antonyms: {str(e)}."

    return antonyms, error_message


def get_pronunciation(data, input_word):
    try:
        pronunciation = data[0]['hwi']['prs'][0].get('mw', f"No pronunciations for the word '{input_word}' were found.")

    except (IndexError, KeyError):
        # Handle the case where 'mw' is missing
        error_message = f"Sorry, we couldn't find any pronunciations for the word '{input_word}'."

    except Exception as e:
        error_message = f"An error occurred while fetching the pronunciation: {str(e)}."

    return pronunciation, error_message


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
        error_message = f"Sorry, we couldn't find any examples for how to use the word '{input_word}'."

    except Exception as e:
        error_message = f"An error occurred while fetching the examples: {str(e)}."

    return examples, error_message


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
        error_message = f"Sorry, the etymology data for the word '{input_word}' does not exist."

    except Exception as e:
        error_message = f"An error occurred while fetching the etymology: {str(e)}."

    return etymology, error_message


if __name__ == '__main__':
    app.run(debug=True, port=5003)
