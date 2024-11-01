from flask import Flask, render_template, request
from word import Word
from flask_caching import Cache

# Set up Flask app and cache configuration
app = Flask(__name__, template_folder='templates')

# Configure the cache
app.config['CACHE_TYPE'] = 'simple'  # You can use 'redis', 'filesystem', etc.
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout (in seconds)
cache = Cache(app)


class UI:
    """
    This class handles the user interface and interactions.
    """

    @app.route('/', methods=['GET', 'POST'])
    def home():
        input_word = ""  # Holds the user-inputted word
        definition = None
        part_of_speech = None
        synonyms = None
        antonyms = None
        pronunciation = None
        examples = None
        etymology = None
        error_message = ""

        if request.method == 'POST':
            input_word = request.form['input_word'].strip()  # Get word from the form

            if not input_word.isalpha():
                error_message = UI.display_error("invalid word")
                return render_template('dictionary_app.html', error_message=error_message)

            action = request.form['action']  # Check which button was pressed

            # Use cache to store API data for the word
            cached_data = cache.get(input_word)
            if cached_data:
                wd = cached_data  # If data is found in the cache, use it
            else:
                wd = Word(word=input_word)  # Otherwise, create a new Word object

                if wd.input_word_data is None:  # Check if the word data is valid
                    error_message = f"No data available for '{input_word}'"
                    return render_template('dictionary_app.html', error_message=error_message)

                cache.set(input_word, wd)  # Cache the valid word object

            try:
                # Perform actions based on the button pressed
                if action == 'definition':
                    definition = wd.get_definition()
                    if not definition or 'Oops' in definition:
                        error_message = definition if definition else "Error fetching definition."
                        definition = None

                elif action == 'pos':
                    part_of_speech = wd.show_part_of_speech()
                    if not part_of_speech or 'Oops' in part_of_speech:
                        error_message = part_of_speech if part_of_speech else "Error fetching part of speech."
                        part_of_speech = None

                elif action == 'synonyms':
                    synonyms = wd.get_synonyms()
                    if not synonyms or 'Oops' in synonyms:
                        error_message = synonyms if synonyms else "Error fetching synonyms."
                        synonyms = None

                elif action == 'antonyms':
                    antonyms = wd.get_antonyms()
                    if not antonyms or 'Oops' in antonyms:
                        error_message = antonyms if antonyms else "Error fetching antonyms."
                        antonyms = None

                elif action == 'pronunciation':
                    pronunciation = wd.get_pronunciation()
                    if not pronunciation or 'Oops' in pronunciation:
                        error_message = pronunciation if pronunciation else "Error fetching pronunciation."
                        pronunciation = None

                elif action == 'examples':
                    examples = wd.provide_examples()
                    if not examples or 'Oops' in examples:
                        error_message = examples if examples else "Error fetching examples."
                        examples = None

                elif action == 'etymology':
                    etymology = wd.show_etymology()
                    if not etymology or 'Oops' in etymology:
                        error_message = etymology if etymology else "Error fetching etymology."
                        etymology = None

            except Exception as e:
                error_message = f"Error: {str(e)}"  # Set the error message here

        return render_template('dictionary_app.html', input_word=input_word,
                               definition=definition, part_of_speech=part_of_speech,
                               synonyms=synonyms, antonyms=antonyms, pronunciation=pronunciation,
                               examples=examples, etymology=etymology, error_message=error_message)

    @staticmethod
    def display_error(message):
        return (f"Oops! It looks like you have entered an {message}. "
                f"Please enter a valid word using alphabetic characters.")


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run Flask app in debug mode on port 5001
