import requests, re


def get_definition(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()

            except ValueError as e:
                print("Invalid JSON format received from the API.")
                return

            # Check if any definitions are available
            if isinstance(data, list) and len(data) > 0:
                try:
                    # Attempt to access the definitions in the response
                    definitions = data[0]['shortdef']

                    print(f"Definition for the word {word}: ")

                    for i, definition in enumerate(definitions, start=1):
                        print(f"{i}. {definition}")
                except KeyError:
                    # Handle the case where 'shortdef' is missing
                    print(f"Sorry, we couldn't find any definitions for the word '{word}'. ")
            else:
                print(f"No definitions for the word {word}.")
        else:
            print(
                f"Oops! Something went wrong while fetching the data. Please try again later. (Error: {response.status_code})")

    except requests.exceptions.Timeout:
        print("It looks like the request took too long. Please check your internet connection and try again later.")

    except requests.exceptions.ConnectionError:
        print("We're having trouble connecting to the dictionary service. "
              "Please check your internet connection and try again later.")

    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}. Please try again later.")


def show_part_of_speech(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError as e:
                print("Invalid JSON format received from the API.")
                return

            # Check if any definitions are available
            if isinstance(data, list) and len(data) > 0:
                try:
                    pos = data[0]['fl']

                    if pos.startswith(('a', 'e', 'i', 'o', 'u')):
                        print(f"The word {word} is an {pos}")
                    else:
                        print(f"The word {word} is a {pos}")
                except KeyError:
                    # Handle the case where 'fl' is missing
                    print(f"Sorry, we couldn't find what part of speech the word '{word}' belongs to.")
            else:
                print(f"The word {word} does not exist.")
        else:
            print(f"Oops! Something went wrong while fetching the data. Please try again later. (Error: {response.status_code})")

    except requests.exceptions.Timeout:
        print("It looks like the request took too long. Please check your internet connection and try again later.")

    except requests.exceptions.ConnectionError:
        print("We're having trouble connecting to the dictionary service. "
              "Please check your internet connection and try again later.")

    except requests.exceptions.RequestException as e:
        print(f"Oops! An unexpected error occurred: {e}. Please try again later.")


def get_synonyms(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError as e:
                print("Invalid JSON format received from the API.")
                return

            # Check if any definitions are available
            if isinstance(data, list) and len(data) > 0:
                try:
                    # Access the first entry in the list
                    syn_list = data[0]['def'][0]['sseq'][0][0][1]['syn_list']
                    print(f"Synonyms for the word {word}: ")

                    for i, syn in enumerate(syn_list[0], 1):
                        print(f"{i}. {syn['wd']}")
                except KeyError:
                    # Handle the case where 'syn_list' is missing
                    print(f"Sorry, we couldn't find any synonyms for the word '{word}'.")
            else:
                print(f"No definitions for the word {word}.")
        else:
            print(f"Oops! Something went wrong while fetching the data. Please try again later. (Error: {response.status_code})")

    except requests.exceptions.Timeout:
        print("It looks like the request took too long. Please check your internet connection and try again later.")

    except requests.exceptions.ConnectionError:
        print("We're having trouble connecting to the dictionary service. "
              "Please check your internet connection and try again later.")

    except requests.exceptions.RequestException as e:
        print(f"Oops! An unexpected error occurred: {e}. Please try again later.")


def get_antonyms(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError as e:
                print("Invalid JSON format received from the API.")
                return

            # Check if any definitions are available
            if isinstance(data, list) and len(data) > 0:
                try:
                    ant_list = data[0]['def'][0]['sseq'][0][0][1]['ant_list']
                    print(f"Antonyms for the word {word}: ")

                    for i, ant in enumerate(ant_list[0], 1):
                        print(f"{i}. {ant['wd']}")
                except KeyError:
                    # Handle the case where 'ant_list' is missing
                    print(f"Sorry, we couldn't find any antonyms for the word '{word}'.")
            else:
                print(f"No definitions for the word {word}.")
        else:
            print(f"Oops! Something went wrong while fetching the data. Please try again later. (Error: {response.status_code})")

    except requests.exceptions.Timeout:
        print("It looks like the request took too long. Please check your internet connection and try again later.")

    except requests.exceptions.ConnectionError:
        print("We're having trouble connecting to the dictionary service. "
              "Please check your internet connection and try again later.")

    except requests.exceptions.RequestException as e:
        print(f"Oops! An unexpected error occurred: {e}. Please try again later.")


def get_pronunciation(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    try:
        response = requests.get(url,  timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError as e:
                print("Invalid JSON format received from the API.")
                return

            # Check if any definitions are available
            if isinstance(data, list) and len(data) > 0:
                try:
                    # Access the third entry in the list
                    mw = data[0]['hwi']['prs'][0]['mw']
                    print(f"The word {word} is pronounced as {mw}.")
                except KeyError:
                    # Handle the case where 'mw' is missing
                    print(f"Sorry, there are no pronunciations for the word '{word}'.")
            else:
                print(f"The word {word} does not exist.")
        else:
            print(f"Oops! Something went wrong while fetching the data. Please try again later. (Error: {response.status_code})")

    except requests.exceptions.Timeout:
        print("It looks like the request took too long. Please check your internet connection and try again later.")

    except requests.exceptions.ConnectionError:
        print("We're having trouble connecting to the dictionary service. "
          "Please check your internet connection and try again later.")

    except requests.exceptions.RequestException as e:
        print(f"Oops! An unexpected error occurred: {e}. Please try again later.")


def provide_examples(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                print("Invalid JSON format received from the API.")
                return

            # Check if any definitions are available
            if isinstance(data, list) and len(data) > 0:
                t_values = []

                print(f"Examples:")
                try:
                    entry = data[0]['quotes']
                    for quote in entry:
                        if 't' in quote:
                            cleaned_t_value = quote['t'].replace("{qword}", "").replace("{/qword}", "")
                            t_values.append(cleaned_t_value)
                    for i, t_value in enumerate(t_values, 1):
                        print(f"{i}. {t_value}")
                except KeyError:
                    # Handle the case where 'quotes' or 't' key is missing
                    print(f"Sorry, we couldn't find any examples for how to use the word '{word}'.")
            else:
                print(f"The word '{word}' does not exist.")
        else:
            print(f"Oops! Something went wrong while fetching the data. Please try again later. (Error: {response.status_code})")

    except requests.exceptions.Timeout:
        print("It looks like the request took too long. Please check your internet connection and try again later.")

    except requests.exceptions.ConnectionError:
        print("We're having trouble connecting to the dictionary service. "
              "Please check your internet connection and try again later.")

    except requests.exceptions.RequestException as e:
        print(f"Oops! An unexpected error occurred: {e}. Please try again later.")


def show_etymology(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError as e:
                print("Invalid JSON format received from the API.")
                return

            # Check if any definitions are available
            if isinstance(data, list) and len(data) > 0:

                entry = data[0]
                # Extract the etymology and date
                try:
                    if 'et' in entry and 'date' in entry:
                        et_entry = entry['et'][0][1]
                        cleaned_etymology = ''.join(et_entry).replace("{it}", "").replace("{/it}", "") # clean the tags

                        # Split by both comma and semicolon in one line using re.split
                        etymology_parts = re.split(r', |; ', cleaned_etymology)

                        print("Etymology:")
                        for i, part in enumerate(etymology_parts, 1):
                            # Print each part on a new line with numbering
                            print(f"{i}. {part}\n")

                        # Print the date
                        date_entry = entry['date']
                        cleaned_date = re.sub(r'\{[^}]*\}', '', date_entry)
                        print(f"Date of origin: {cleaned_date.strip()}")
                    else:
                        print(f"The word {word} does not exist.")
                except KeyError:
                    # Handle the case where 'et' or 'date' keys are missing
                    print(f"Sorry, the etymology data for the word '{word}' does not exist")
            else:
                print(f"The word {word} does not exist.")
        else:
            print(f"Oops! Something went wrong while fetching the data. Please try again later. (Error: {response.status_code})")

    except requests.exceptions.Timeout:
        print("It looks like the request took too long. Please check your internet connection and try again later.")

    except requests.exceptions.ConnectionError:
        print("We're having trouble connecting to the dictionary service. "
              "Please check your internet connection and try again later.")

    except requests.exceptions.RequestException as e:
        print(f"Oops! An unexpected error occurred: {e}. Please try again later.")


api_keys = ["47a18b32-61c5-4951-ad64-1fdbbf295a5d", "864ede40-eae9-41c8-98c3-c24c92e8dd4e"]

word = "family"

get_definition(word=word, api_key=api_keys[0])

show_part_of_speech(word=word, api_key=api_keys[1])

get_synonyms(word=word, api_key=api_keys[0])

get_antonyms(word=word, api_key=api_keys[0])

get_pronunciation(word=word, api_key=api_keys[1])

provide_examples(word=word, api_key=api_keys[1])

show_etymology(word=word, api_key=api_keys[1])