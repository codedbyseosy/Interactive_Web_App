import re
from dictionaryapi import DictionaryAPI


class Word:
    """
    This class represents a word with attributes like
    definition, synonyms, antonyms, etc.
    """
    def __init__(self, word):
        self.word = word  # Store the input word
        self.da = DictionaryAPI()  # Create an instance of the DictionaryAPI
        self.input_word_data = self.fetch_word_data()  # Fetch data for the word

    def fetch_word_data(self):
        """
        Fetch word data from the DictionaryAPI class.
        """
        data = self.da.fetch_word_data(self.word)  # Get data for the word

        # Ensure that the data is a tuple and the first two elements exist
        if isinstance(data, tuple) and len(data) >= 2 and data[0] and data[1]:
            return data  # Return the valid data
        else:
            return None  # Return None if the data is invalid

    def get_definition(self):
        """
        Method to retrieve and return the definition of the input word.
        """
        if not self.input_word_data:
            return f"Oops! We could not find any data for the word '{self.word}'. Please try again later."

        try:
            definitions = self.input_word_data[0][0].get('shortdef', [])  # Get definitions

            if not definitions:
                return f"No definitions for the word '{self.word}' were found."

            # Append each definition to the 'definition' string
            return '<br><br>'.join(f"{i}. {defn}" for i, defn in enumerate(definitions, 1))
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def show_part_of_speech(self):
        """
        Method to retrieve and return what part of speech the input word belongs to.
        """
        if not self.input_word_data:
            return f"Oops! We could not find any data for the word '{self.word}'. Please try again later."

        try:
            part_of_speech = self.input_word_data[1][0].get('fl', [f"The word '{self.word}' does not belong to any part of speech."])

            if not part_of_speech:
                return f"Apologies, we were unable to find what part of speech the word '{self.word}' belongs to."

            return part_of_speech  # Return part of speech
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def get_synonyms(self):
        """
        Method to retrieve and return the synonyms of the input word.
        """
        if not self.input_word_data:
            return (f"Oops! We could not find any data for the word '{self.word}'. "
                    f"Please try again later.")
        try:
            synonyms_list = self.input_word_data[0][0].get('def', [{}])[0].get('sseq', [[]])[0][0][1].get('syn_list', [])

            if not synonyms_list:
                return f"No synonyms for the word '{self.word}' were found."

            # Format and return the list of synonyms
            return '<br><br>'.join(f"{i}. {syn['wd']}" for i, syn in enumerate(synonyms_list[0], 1))
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def get_antonyms(self):
        """
        Method to retrieve and return the antonyms of the input word.
        """
        if not self.input_word_data:
            return (f"Oops! We could not find any data for the word '{self.word}'. "
                    f"Please try again later.")
        try:
            antonyms_list = self.input_word_data[0][0].get('def', [{}])[0].get('sseq', [[]])[0][0][1].get('ant_list', [])

            if not antonyms_list:
                return f"No antonyms for the word '{self.word}' were found."

            # Format and return the list of antonyms
            return '<br><br>'.join(f"{i}. {ant['wd']}" for i, ant in enumerate(antonyms_list[0], 1))
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def get_pronunciation(self):
        """
        Method to retrieve and return the pronunciation of the input word.
        """
        if not self.input_word_data:
            return (f"Oops! We could not find any data for the word '{self.word}'. "
                    f"Please try again later.")
        try:
            # Retrieve pronunciation data
            return self.input_word_data[1][0]['hwi']['prs'][0].get('mw',
                                                         f"No pronunciations for the word '{self.word}' were found.")
        except Exception as e:
            # Handle any other unexpected errors
            return self.da.handle_errors(e)

    def provide_examples(self):
        """
        Method to retrieve and return examples of how the input word is used.
        """
        if not self.input_word_data:
            return (f"Oops! We could not find any data for the word '{self.word}'. "
                    f"Please try again later.")

        try:
            # Check if 'quotes' exist in the data
            quotes = self.input_word_data[1][0].get('quotes', [])

            if quotes:  # If quotes exist, process them
                return '<br><br>'.join(f"{i}. {re.sub(r'\{qword\}|\{/qword\}', '', quote['t'])}"
                                       for i, quote in enumerate(quotes, 1)
                                       if isinstance(quote, dict) and 't' in quote)

            # If 'quotes' do not exist, check the 'def' section for 'vis' entries
            def_section = self.input_word_data[1][0].get('def', [])
            examples = []

            if def_section:
                # Traverse the def section for examples (usually in the 'vis' key)
                for entry in def_section:
                    # Navigate to the examples (if any) stored under 'vis'
                    sense = entry.get('sseq', [[]])[0][0][1].get('dt', [])
                    for d in sense:
                        if d[0] == 'vis':  # 'vis' typically contains examples
                            for vis_entry in d[1]:
                                example_text = vis_entry.get('t', '')
                                # Clean up the {qword} markers and format example
                                cleaned_example = re.sub(r'\{wi\}|\{/wi\}', '', example_text)
                                examples.append(cleaned_example)

                # Format the examples for display
                if examples:
                    return '<br><br>'.join(f"{i}. {example}" for i, example in enumerate(examples, 1))

            return f"No examples for the word '{self.word}' were found."

        except Exception as e:
            # Handle any other unexpected errors
            return f"Oops! An unexpected error occurred: {str(e)}. Please try again later."

    def show_etymology(self):
        """
        Method to retrieve and return the etymology data of the input word.
        """
        if not self.input_word_data:
            return (f"Oops! We could not find any data for the word '{self.word}'. "
                    f"Please try again later.")
        try:
            # Fetch the etymology data
            et_data = self.input_word_data[1][0].get('et', [])

            if et_data and isinstance(et_data[0], list):
                et = et_data[0][1]  # Extract etymology if it exists
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
            return self.da.handle_errors(e)
