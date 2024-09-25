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
                print(f"Definition for the word {word}: ")

                for i, definition in enumerate(definitions, start=1):
                    print(f"{i}. {definition}")
            else:
                print(f"No definitions for the word {word}.")
        else:
            print(f"No definitions for the word {word}.")
    else:
        print('Error:', response.status_code)


api_key = "47a18b32-61c5-4951-ad64-1fdbbf295a5d"

word = "friend"

get_definition(word=word, api_key=api_key)
