import re
from dictionaryapi import DictionaryAPI


class Word:
    """
    This class represents a word with attributes like
    definition, synonyms, antonyms, etc.
    """
    def __init__(self, input_word):
        self.input_word = input_word
        self.da = DictionaryAPI()
        self.input_word_data = self.fetch_word_data()

    def fetch_word_data(self):
        data = self.da.fetch_word_data(self.input_word)
        if isinstance(data, list) and data[0] is not None:
            return data
        else:
            print(data)

    def get_definition(self):
        """
        Method to retrieve and return the definition
        of the input word
        """

        try:
            definitions = self.input_word_data[0][0].get('shortdef', [])

            if not definitions:
                return f"No definitions for the word '{self.input_word}' were found."

            # Append each definition to the 'definition' string
            return '<br><br>'.join(f"{i}. {defn}" for i, defn in enumerate(definitions, 1))
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors("definition")

    def show_part_of_speech(self):
        """
        Method to retrieve and return what part of
        speech the input word belongs to
         """
        try:
            return self.input_word_data[1][0].get('fl', [f"The word '{self.input_word}' does not belong to"
                                                                f" any part of speech."])
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def get_synonyms(self):
        """
        Method to retrieve and return the synonyms
        of the input word
         """
        try:
            synonyms_list = self.input_word_data[0][0].get('def', [{}])[0].get('sseq', [[]])[0][0][1].get('syn_list', [])

            if not synonyms_list:
                return f"No synonyms for the word '{self.input_word}' were found."

            return '<br><br>'.join(f"{i}. {syn['wd']}" for i, syn in enumerate(synonyms_list[0], 1))
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def get_antonyms(self):
        """
             Method to retrieve and return the antonyms
             of the input word
         """
        try:
            antonyms_list = self.input_word_data[0][0].get('def', [{}])[0].get('sseq', [[]])[0][0][1].get('ant_list', [])

            if not antonyms_list:
                return f"No antonyms for the word '{self.input_word}' were found."

            return '<br><br>'.join(f"{i}. {ant['wd']}" for i, ant in enumerate(antonyms_list[0], 1)
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def get_pronunciation(self):
        """
             Method to retrieve and return the pronunciation
             of the input word
         """
        try:
            return self.input_word_data[1][0]['hwi']['prs'][0].get('mw',
                                                         f"No pronunciations for the word '{self.input_word}' were found.")
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def provide_examples(self):
        """
             Method to retrieve and return the examples
            for how the input word is used
         """
        try:
            quotes = self.input_word_data[1][0].get('quotes', [])

            if not quotes:
                return f"No examples for the word '{self.input_word}' were found."
            return '<br><br>'.join(f"{i}. {quote['t'].replace('{qword)', '').replace('{/qword)', '')}"
                                   for i, quote enumerate(quotes, 1)
                                   if isinstance(quote, dict) and 't' in quote)
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def show_etymology(self):
        """
         Method to retrieve and return the etymology data
         of the input word
         """
        try:
            # Fetch the etymology data
            et_data = self.input_word_data[1][0].get('et', [])

            if et_data and isinstance(et_data[0], list):
                et = et_data[0][1]
            else:
                et = et_data[0] if isinstance(et_data, list) else ""

            # Clean up the curly braces and content within them
            cleaned_etymology = re.sub(r'\{[^}]*\}', '', et)

            # Split by both comma and semicolon in one line using re.split
            etymology_parts = re.split(r', |; ', cleaned_etymology)

            # Fetch and clean the date data
            date_entry = self.input_word_data[1][0].get('date', 'No date available')
            cleaned_date = re.sub(r'\{[^}]*\}', '', date_entry)

            # Format each part with numbering and <br> for HTML line breaks
            return '<br><br>'.join(f"{i}. {part}" for i, part in enumerate(etymology_parts, 1)), cleaned_date

        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors("etymology")




