from flask import Flask, render_template, request
import requests
from word import Word
from dictionaryapi import DictionaryAPI

app = Flask(__name__)


class UI:
    """
    This class handles the user interface and interactions.
    """
    @app.route('/', methods=['GET', 'POST'])
    def home():
        """
        This route handles the display of the dictionary's word data
        and manages form submission for various actions related to words.
        """

        input_word = ""  # Holds the user-inputted word
        definition = None  # Holds the word's definition
        part_of_speech = None  # Holds the part of speech for the word
        synonyms = None  # Holds a list of synonyms for the word
        antonyms = None  # Holds a list of antonyms for the word
        pronunciation = None  # Holds the pronunciation of the word
        examples = None  # Holds example sentences using the word
        etymology = None  # Holds the word's origin and history
        error_message = None  # To hold any error messages

        if request.method == 'POST':
            input_word = request.form['input_word']  # Get the word input from the form

            da = DictionaryAPI()  # Create an instance of DictionaryAPI
            wd = Word(word=input_word)  # Create an instance of Word with the input word

            if not input_word.isalpha():
                # Validate that the input is alphabetic
                error_message = UI.display_error("Invalid word")  # Set error message
                return render_template('dictionary_app.html', error_message=error_message)

            action = request.form['action']  # Check which button has been pressed

            # Perform actions based on the button pressed
            if action == 'definition':
                definition = wd.get_definition()  # Get word definition

            elif action == 'pos':
                part_of_speech = wd.show_part_of_speech()  # Get part of speech

            elif action == 'synonyms':
                synonyms = wd.get_synonyms()  # Get synonyms

            elif action == 'antonyms':
                antonyms = wd.get_antonyms()  # Get antonyms

            elif action == 'pronunciation':
                pronunciation = wd.get_pronunciation()  # Get pronunciation

            elif action == 'examples':
                examples = wd.provide_examples()  # Get example sentences

            elif action == 'etymology':
                etymology = wd.show_etymology()  # Get etymology

        # Render the template with the gathered data
        return render_template(
            'dictionary_app.html', input_word=input_word,
            definition=definition, part_of_speech=part_of_speech,
            synonyms=synonyms, antonyms=antonyms, pronunciation=pronunciation,
            examples=examples, etymology=etymology, error_message=error_message)

    @staticmethod
    def display_error(message):
        # Static method that returns an error message
        return f"{message}. Please enter a valid word using alphabetic characters."


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run the Flask app in debug mode on port 5001
