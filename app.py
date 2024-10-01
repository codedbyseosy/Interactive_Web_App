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
                    data = response.json()
                    definition = get_definition(data, input_word)
                else:
                    error_message = 'Error fetching definition.'

            # If the user presses the 'Show part of speech' button
            elif action == 'pos':
                response = requests.get(urls['collegiate'], timeout=200)
                if response.status_code == 200:
                    data = response.json()
                    part_of_speech = show_part_of_speech(data, input_word)
                else:
                    error_message = 'Error fetching the parts of speech.'

            # If the user presses the 'Get synonyms' button
            elif action == 'synonyms':
                response = requests.get(urls['thesaurus'], timeout=200)
                if response.status_code == 200:
                    data = response.json()
                    synonyms = get_synonyms(data, input_word)
                else:
                    error_message = 'Error fetching synonyms.'

            # If the user presses the 'Get antonyms' button
            elif action == 'antonyms':
                response = requests.get(urls['thesaurus'], timeout=200)
                if response.status_code == 200:
                    data = response.json()
                    antonyms = get_antonyms(data, input_word)
                else:
                    error_message = 'Error fetching antonyms.'

            # If the user presses the 'Get pronunciation' button
            elif action == 'pronunciation':
                response = requests.get(urls['collegiate'], timeout=200)
                if response.status_code == 200:
                    data = response.json()
                    pronunciation = get_pronunciation(data, input_word)
                else:
                    error_message = 'Error fetching pronunciations.'

            # If the user the presses the 'Provide examples' button
            elif action == 'examples':
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    data = response.json()
                    examples = provide_examples(data, input_word)
                else:
                    error_message = 'Error fetching examples.'

            # If the user the presses the 'Show etymology' button
            elif action == 'etymology':
                response = requests.get(urls['collegiate'], timeout=200)

                if response.status_code == 200:
                    data = response.json()
                    etymology = show_etymology(data, input_word)
                else:
                    error_message = 'Error fetching etymology.'

        except TypeError:
            error_message = ("Oops! We received unexpected data from the dictionary service. "
                             "Please try again later or check the word you're looking up.")

        except requests.exceptions.Timeout:
            error_message = ("It looks like the request took too long. "
                             "Please check your internet connection and try again later. ")

        except requests.exceptions.ConnectionError:
            error_message = ("We're having trouble connecting to the dictionary service. "
                             "Please check your internet connection and try again later.")

        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred: {e}. Please try again later.")

    return render_template('dictionary_app.html',
                           input_word=input_word,
                           definition=definition, pos=part_of_speech, synonyms=synonyms, antonyms=antonyms,
                           pronunciation=pronunciation, examples=examples, etymology=etymology)


def get_definition(data, input_word):
    try:
        definitions = data[0].get('shortdef', [])

        if not definitions:
            return f"No definitions for the word '{input_word}' were found."

        definition = ''
        for i, defn in enumerate(definitions, 1):
            # Append each definition to the 'definition' string
            definition += f"{i}. {defn}<br><br>"
        return definition

    except (IndexError, KeyError):
        # Handle the case where 'shortdef' is missing
        return f"Sorry, no definitions for the word '{input_word}' were found."

    except Exception as e:
        return f"An error occurred while fetching the definition: {str(e)}."


def show_part_of_speech(data, input_word):
    try:
        part_of_speech = data[0].get('fl', [f"The word '{input_word}' does not belong to any part of speech."])
        return part_of_speech

    except (IndexError, KeyError):
        # Handle the case where 'fl' is missing
        return f"Sorry, we couldn't find what part of speech the word '{input_word}' belongs to."

    except Exception as e:
        return f"An error occurred while fetching the part of speech: {str(e)}."


def get_synonyms(data, input_word):
    try:
        synonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('syn_list', [])

        if not synonyms_list:
            return f"No synonyms for the word '{input_word}' were found."

        synonyms = ''
        for i, syn in enumerate(synonyms_list[0], 1):
            synonyms += f"{i}. {syn['wd']}<br><br>"
        return synonyms

    except (IndexError, KeyError):
        # Handle the case where 'syn_list' is missing
        return f"Sorry, we couldn't find any synonyms for the word '{input_word}'."

    except Exception as e:
        return f"An error occurred while fetching the synonyms: {str(e)}."


def get_antonyms(data, input_word):
    try:
        antonyms_list = data[0]['def'][0]['sseq'][0][0][1].get('ant_list', [])

        if not antonyms_list:
            return f"No antonyms for the word '{input_word}' were found."

        antonyms = ''
        for i, ant in enumerate(antonyms_list[0], 1):
            antonyms += f"{i}. {ant['wd']}<br><br>"
        return antonyms

    except (IndexError< KeyError):
        # Handle the case where 'ant_list' is missing
        return f"Sorry, we couldn't find any antonyms for the word '{input_word}'."

    except Exception as e:
        return f"An error occurred while fetching the antonyms: {str(e)}."


def get_pronunciation(data, input_word):
    try:
        pronunciation = data[0]['hwi']['prs'][0].get('mw', f"No pronunciations for the word '{input_word}' were found.")
        return pronunciation

    except (IndexError, KeyError):
        # Handle the case where 'mw' is missing
        return f"Sorry, we couldn't find any pronunciations for the word '{input_word}'."

    except Exception as e:
        return f"An error occurred while fetching the pronunciation: {str(e)}."


def provide_examples(data, input_word):
    try:
        quotes = data[0].get('quotes', [])

        if not quotes:
            return f"No examples for the word '{input_word}' were found."

        examples = ''
        for i, quote in enumerate(quotes, 1):
            if isinstance(quote, dict) and 't' in quote:
                cleaned_t_value = quote['t'].replace("{qword}", "").replace("{/qword}", "")
                examples += f"{i}. {cleaned_t_value}<br><br>"

        if not examples:
            return 'No examples found.'

        return examples

    except (IndexError, KeyError):
        # Handle the case where 'quotes' or 't' key is missing
        return f"Sorry, we couldn't find any examples for how to use the word '{input_word}'."

    except Exception as e:
        return f"An error occurred while fetching the examples: {str(e)}."


def show_etymology(data, input_word):
    try:
        etymology = ""

        # Fetch the etymology data
        et_data = data[0].get('et', [])

        if et_data and isinstance(et_data[0], list):
            et = et_data[0][1]
        else:
            et = et_data[0] if isinstance(et_data, list) else ""

        # Clean up the curly braces and content within them
        cleaned_etymology = re.sub(r'\{[^}]*\}', '', et)

        # Split by both comma and semicolon in one line using re.split
        etymology_parts = re.split(r', |; ', cleaned_etymology)

        # Format each part with numbering and <br> for HTML line breaks
        et_entry = ""
        for i, part in enumerate(etymology_parts, 1):
            et_entry += f"{i}. {part}<br><br>"

        # Fetch and clean the date data
        date_entry = data[0].get('date', 'No date available')
        cleaned_date = re.sub(r'\{[^}]*\}', '', date_entry)

        # Return the etymology and cleaned date as a tuple
        return et_entry, cleaned_date

    except (IndexError, KeyError):
        # Handle the case where 'et' or 'date' keys are missing
        return f"Sorry, the etymology data for the word '{input_word}' does not exist."

    except Exception as e:
        # Handle any other unexpected errors
        return f"An error occurred while fetching the etymology: {str(e)}."

if __name__ == '__main__':
    app.run(debug=True, port=5003)
