import requests, re


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


def show_part_of_speech(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            entry = data[0]

            if 'fl' in entry:
                pos = entry['fl']
                print(f"The word {word} is a {pos}")
            else:
                print(f"The word {word} does not exist.")
        else:
            print(f"The word {word} does not exist.")
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
            print(f"Synonyms for the word {word}: ")

            for i, syn in enumerate(syn_list[0], 1):
                print(f"{i}. {syn['wd']}")
                #synonyms.append(syn['wd'])

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

            ant_list = data[0]['def'][0]['sseq'][0][0][1]['ant_list']
            print(f"Antonyms for the word {word}: ")

            for i, ant in enumerate(ant_list[0], 1):
                print(f"{i}. {ant['wd']}")
                #antonyms.append(ant['wd'])

        else:
            print(f"No definitions for the word {word}.")
    else:
        print('Error:', response.status_code)


def get_pronunciation(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        #print(data)

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

            print(f"The word {word} is used correctly in the following examples:")
            if 'quotes' in entry:
                for quote in entry['quotes']:
                    if 't' in quote:
                        cleaned_t_value = quote['t'].replace("{qword}", "").replace("{/qword}", "")
                        t_values.append(cleaned_t_value)
                        for i, t_value in enumerate(t_values, 1):
                            examples = f"{i}. {t_value}"
                    print(examples)
            else:
                print(f"The word {word} does not exist.")

        else:
            print(f"The word {word} does not exist.")
    else:
        print('Error:', response.status_code)


def show_etymology(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)

        # Check if any definitions are available
        if isinstance(data, list) and len(data) > 0:

            entry = data[0]
            # Extract the etymology and date
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
                print(f"Date: {date_entry}")
            else:
                print(f"The word {word} does not exist.")
        else:
            print(f"The word {word} does not exist.")
    else:
        print('Error:', response.status_code)


api_keys = ["47a18b32-61c5-4951-ad64-1fdbbf295a5d", "864ede40-eae9-41c8-98c3-c24c92e8dd4e"]

word = "friend"

get_definition(word=word, api_key=api_keys[0])

show_part_of_speech(word=word, api_key=api_keys[1])

get_synonyms(word=word, api_key=api_keys[0])

get_antonyms(word=word, api_key=api_keys[0])

get_pronunciation(word=word, api_key=api_keys[1])

provide_examples(word=word, api_key=api_keys[1])

show_etymology(word=word, api_key=api_keys[1])