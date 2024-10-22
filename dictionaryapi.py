import requests


class DictionaryAPI:
    """
    This class handles API requests and responses to fetch word data.
    """

    def __init__(self):
        # List of API keys for accessing the dictionary service
        self.api_keys = ["47a18b32-61c5-4951-ad64-1fdbbf295a5d", "864ede40-eae9-41c8-98c3-c24c92e8dd4e"]

        # Base URLs for thesaurus and collegiate dictionary endpoints
        self.base_url = {
            "thesaurus": "https://www.dictionaryapi.com/api/v3/references/thesaurus/json",
            "collegiate": "https://www.dictionaryapi.com/api/v3/references/collegiate/json"
        }

    def fetch_word_data(self, input_word):
        """
        Fetches word data from both thesaurus and collegiate dictionary APIs.
        """
        # Construct the URLs for the API requests
        thesaurus_url = f"{self.base_url['thesaurus']}/{input_word}?key={self.api_keys[0]}"
        collegiate_url = f"{self.base_url['collegiate']}/{input_word}?key={self.api_keys[1]}"

        try:
            # Make API requests to both thesaurus and collegiate endpoints
            thesaurus_response = requests.get(thesaurus_url, timeout=200)
            collegiate_response = requests.get(collegiate_url, timeout=200)

            # Raise an exception if the status code is not 200
            thesaurus_response.raise_for_status()
            collegiate_response.raise_for_status()

            # Get the JSON data from the responses
            thesaurus_data = thesaurus_response.json()
            collegiate_data = collegiate_response.json()

            return thesaurus_data, collegiate_data  # Return the fetched data

        except TypeError:
            # Handle unexpected data types in the response
            error_message = ("Oops! We received unexpected data from the dictionary service. "
                             "Please try again later or check the word you're looking up.")
            return self.handle_errors(error_message)

        except requests.exceptions.Timeout:
            # Handle timeout errors
            error_message = ("It looks like the request took too long. "
                             "Please check your internet connection and try again later.")
            return self.handle_errors(error_message)

        except requests.exceptions.ConnectionError:
            # Handle connection errors
            error_message = ("We're having trouble connecting to the dictionary service. "
                             "Please check your internet connection and try again later.")
            return self.handle_errors(error_message)

        except requests.exceptions.RequestException as e:
            # Handle any other request-related errors
            return self.handle_errors(e)

    @staticmethod
    def handle_errors(error):
        """
        Handles any API-related errors by returning a formatted error message.
        """
        return error
