import requests
import json

# syns_list = data[0]['meta']['def'][0]['sseq'][0][0]['syn_list']


def get_definition(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            # Access the first entry in the list
            entry = data[0]

            # Check if definitions are available
            if 'shortdef' in entry:
                definitions = entry['shortdef']
                # print(data)
                print(f"Definition for the word {word}: ")

                for i, definition in enumerate(definitions, start=1):
                    print(f"{i}. {definition}")
            else:
                print(f"No definitions for the word {word}.")
        else:
            print(f"No definitions for the word {word}.")
    else:
        print('Error:', response.status_code)


def get_synonym(word, api_key):
    pass


def get_antonym(word, api_key):
    pass


def get_pronunciation(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            # Access the third entry in the list
            entry = data[0]

            if 'hwi' in entry:
                headword = entry['hwi']

                if 'prs' in headword:
                    # print(f"Pronunciation exists for the word {word}.")

                    new_entry = headword['prs'][0]

                    if 'mw' in new_entry:
                        mw = new_entry['mw']
                        print(f"The word {word} is pronounced as {mw}.")

                    else:
                        print(f"The word {word} does not exist.")
                else:
                    print(f"The word {word} does not exist.")

            else:
                print(f"The word {word} does not exist.")
        else:
            print(f"The word {word} does not exist.")
    else:
        print('Error:', response.status_code)


def provide_examples(word, api_key):
    pass


api_keys = ["47a18b32-61c5-4951-ad64-1fdbbf295a5d", "864ede40-eae9-41c8-98c3-c24c92e8dd4e"]

word = "friend"

get_definition(word=word, api_key=api_keys[0])

get_pronunciation(word=word, api_key=api_keys[1])