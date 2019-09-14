import json

aspects_path = 'opinion_mining/aspects.json'

aspects = json.loads(open(aspects_path, 'r').read())


def find_aspects(text, product_type):
    aspects_found = []

    # Split text into words, removing ponctuation
    words = text.lower().replace(',', ' ').replace(':', ' ').replace(';', ' ').replace('.', ' ').replace('-', ' ').split()

    product_key = product_type.lower()

    for word in words:

        aspect = ''

        # Searches in the list of aspects of the specific type of product 
        if word in aspects[product_key].values():
            aspect = word

        # If still not found, searches in the aspects clues of the specific type of product 
        elif word in aspects[product_key]:
            aspect = aspects[product_key][word]

        # If still not found, searches in the list of generic aspects
        elif word in aspects['GENERIC'].values():
            aspect = word

        # If still not found, searches in the list of generic clues
        elif word in aspects['GENERIC']:
            aspect = aspects['GENERIC'][word]

        aspect = aspect.upper()

        if aspect != '' and aspect not in aspects_found:
            aspects_found.append(aspect)

    if aspects_found == []:
        aspects_found = [aspects['GENERIC']['_GENERIC_'].upper()]  # Label for opinions about the entity as a whole (usually "produto" in Portuguese)

    return aspects_found
