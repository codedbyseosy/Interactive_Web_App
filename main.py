import requests


def get_definition(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            # Access the first entry in the list
            definitions = data[0]['shortdef']

            print(f"Definition for the word {word}: ")

            for i, definition in enumerate(definitions, start=1):
                print(f"{i}. {definition}")
        else:
            print(f"No definitions for the word {word}.")
    else:
        print('Error:', response.status_code)


def get_synonyms(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            # Access the first entry in the list
            syn_list = data[0]['def'][0]['sseq'][0][0][1]['syn_list']
            synonyms = []
            for syn in syn_list[0]:
                synonyms.append(syn['wd'])

            print(f"The synonyms for the word {word} are: {synonyms}")

        else:
            print(f"No definitions for the word {word}.")
    else:
        print('Error:', response.status_code)


def get_antonyms(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            # Access the first entry in the list
            # ant_list = data[0]['def'][0]['sseq'][0][0][1]['ant_list']
            #if 'ant_list' in data[0]['def'][0]['sseq'][0][0][1]:
            ant_list = data[0]['def'][0]['sseq'][0][0][1]['ant_list']

            antonyms = []
            for ant in ant_list[0]:
                antonyms.append(ant['wd'])

            print(f"The antonyms for the word {word} are: {antonyms}")
            # else:
            #     print(f"No definitions for the word {word}.")
        else:
            print(f"No definitions for the word {word}.")
    else:
        print('Error:', response.status_code)


def get_pronunciation(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            # Access the third entry in the list
            mw = data[0]['hwi']['prs'][0]['mw']
            print(f"The word {word} is pronounced as {mw}.")

        else:
            print(f"The word {word} does not exist.")
    else:
        print('Error:', response.status_code)


def provide_examples(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:
            t_values = []
            entry = data[0]

            if 'quotes' in entry:
                for quote in entry['quotes']:
                    if 't' in quote:
                        t_values.append(quote['t'])
                print(t_values)
            else:
                print(f"The word {word} does not exist.")

        else:
            print(f"The word {word} does not exist.")
    else:
        print('Error:', response.status_code)


api_keys = ["47a18b32-61c5-4951-ad64-1fdbbf295a5d", "864ede40-eae9-41c8-98c3-c24c92e8dd4e"]

word = "grateful"

get_definition(word=word, api_key=api_keys[0])

get_synonyms(word=word, api_key=api_keys[0])

get_antonyms(word=word, api_key=api_keys[0])

get_pronunciation(word=word, api_key=api_keys[1])

provide_examples(word=word, api_key=api_keys[1])