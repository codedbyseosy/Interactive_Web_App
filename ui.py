from flask import Flask, render_template, request
from word import Word
from flask_caching import Cache

# Set up Flask app and cache configuration
app = Flask(__name__, template_folder='templates')

# Configure the cache
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/0"
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
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
        error_message = None

        if request.method == 'POST':
            try:
                input_word = request.form['input_word']  # Get word from the form

                if not input_word.isalpha():
                    error_message = UI.display_error("invalid word")
                    return render_template('dictionary_app.html', error_message=error_message)

                action = request.form['action']  # Check which button was pressed

                # Use cache to store API data for the word
                cached_data = cache.get(input_word)
                if cached_data:
                    # If data is found in the cache, use it
                    wd = cached_data
                else:
                    # Otherwise, create a new Word object and cache the result
                    wd = Word(word=input_word)
                    cache.set(input_word, wd)  # Cache the word object

                # Perform actions based on the button pressed
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

        return render_template('dictionary_app.html', input_word=input_word,
                               definition=definition, part_of_speech=part_of_speech,
                               synonyms=synonyms, antonyms=antonyms, pronunciation=pronunciation,
                               examples=examples, etymology=etymology, error_message=error_message)

    @staticmethod
    def display_error(message):
        return f"Oops! It looks like you have entered an {message}. Please enter a valid word using alphabetic characters."


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run Flask app in debug mode on port 5001
