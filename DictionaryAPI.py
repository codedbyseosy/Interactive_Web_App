import Word as wd
import requests


class DictionaryAPI:
    """
    This class handles API requests and responses.
    """
    def __init__(self):
        self.api_keys = ["47a18b32-61c5-4951-ad64-1fdbbf295a5d", "864ede40-eae9-41c8-98c3-c24c92e8dd4e"]
        self.base_url = {
            "thesaurus": "https://www.dictionaryapi.com/api/v3/references/thesaurus/json",
            "collegiate": "https://www.dictionaryapi.com/api/v3/references/collegiate/json"
        }

    def fetch_word_data(self, input_word):
        thesaurus_url = f"{self.base_url['thesaurus']}/{input_word.wd.word}?key={self.api_keys[0]}"
        collegiate_url = f"{self.base_url['collegiate']}/{input_word.wd.word}?key={self.api_keys[1]}"

        try:
            # Make API requests to both thesaurus and collegiate endpoints
            thesaurus_response = requests.get(thesaurus_url)
            collegiate_response = requests.get(collegiate_url)

            # Raise an exception if the status code is not 200
            thesaurus_response.raise_for_status()
            collegiate_response.raise_for_status()

            return thesaurus_response.json(), collegiate_response.json()

        except TypeError:
            return "Oops! We received unexpected data from the dictionary service. Please try again later or check the word you're looking up."

        except requests.exceptions.Timeout:
            return "It looks like the request took too long. Please check your internet connection and try again later."

        except requests.exceptions.ConnectionError:
            return "We're having trouble connecting to the dictionary service. Please check your internet connection and try again later."

        except requests.exceptions.RequestException as e:
            return self.handle_errors(e)

    def handle_errors(self, error):
        """
        Handles any API-related errors.
        """
        return f"An unexpected error occurred: {error}. Please try again later."
