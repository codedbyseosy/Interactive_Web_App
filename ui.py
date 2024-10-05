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
        This route handles the display of the dictionary's word data and handles form submission.
        """

        input_word = ""
        definition = None
        part_of_speech = None
        synonyms = None
        antonyms = None
        pronunciation = None
        examples = None
        etymology = None
        error_message = None  # To hold any error messages

        if request.method == 'POST':
            input_word = request.form['input_word']

            da = DictionaryAPI()

            wd = Word(input_word=input_word)

            if not input_word.isalpha():
                error_message = UI.display_error("Invalid word")
                return render_template('dictionary_app.html', error_message=error_message)

            action = request.form['action']  # Check which button has been pressed

            if action == 'definition':
                definition = wd.get_definition()

            elif action == 'pos':
                part_of_speech = wd.show_part_of_speech()

            elif action == 'synonyms':
                synonyms = wd.get_synonyms()

            elif action == 'antonyms':
                antonyms = wd.get_antonyms()

            elif action == 'pronunciation':
                pronunciation = wd.get_pronunciation()

            elif action == 'examples':
                examples = wd.provide_examples()

            elif action == 'etymology':
                etymology = wd.show_etymology()

        return render_template(
            'dictionary_app.html', input_word=input_word,
            definition=definition, part_of_speech=part_of_speech,
            synonyms=synonyms, antonyms=antonyms, pronunciation=pronunciation,
            examples=examples, etymology=etymology, error_message=error_message)

    @staticmethod
    def display_error(message):
        # Static method that doesn't rely on instance attributes
        return f"{message}. Please enter a valid word using alphabetic characters."


if __name__ == '__main__':
    app.run(debug=True, port=5001)