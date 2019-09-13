DIR_save = 'output'
DIR_read = 'input'

from datetime import datetime

import read_data

from opinion_mining.aspects import find_aspects
from opinion_mining.polarity import get_polarity

from format_output import make_overview_table
from format_output import unikey

SENTENCE_BEGIN_INDICATOR = '::'


# Write text in the dataset
def write_data(destination, text):
    destination.write(str(text))
    print('\033[92m' + text.replace('\n', '') + '\033[0m')


# Save a review sentence to the dataset 
def save_sentence(destination, entry_id, text, polarity='', aspects=''):
    formatted_aspects = '%-20s' % ('[' + str(' '.join(word for word in aspects)) + ']')

    write_data(destination, entry_id + '  ' + polarity + formatted_aspects + SENTENCE_BEGIN_INDICATOR + '  ' + text)
    write_data(destination, '\n\n')


products_data = read_data.read(DIR_read)

current_time = datetime.now()

import os

if not os.path.exists(DIR_save):
    os.makedirs(DIR_save)

for product_data in products_data:

    meta = product_data['meta']
    data = product_data['data']

    product_id = meta['ID']

    output_path = DIR_save + '/' + str(product_id) + '.txt'

    reviews_address = meta['Source']

    product_name = meta['Product']

    product_type = meta['Type']

    total_reviews = meta['Number of reviews']

    avg_rating = meta['Average rating']

    collection_date = meta['Collection date']

    output_file = open(output_path, 'w')

    write_data(output_file, "> ID:  " + str(product_id) + '\n\n')
    write_data(output_file, "> Type:  " + str(product_type).capitalize() + '\n\n')
    write_data(output_file, "> Product:  " + product_name + '\n\n')
    write_data(output_file, "> Average rating:  " + avg_rating + '\n\n')
    write_data(output_file, "> Number of reviews:  " + str(total_reviews) + '\n\n')
    write_data(output_file, "> Collection date:  " + collection_date + '\n\n')
    write_data(output_file, "> Processing date:  " + str(current_time.strftime("%Y-%m-%d")) + '\n\n')
    write_data(output_file, "> Source:  " + str(reviews_address) + '\n\n')
    write_data(output_file, '\n')

    data_to_write = []

    for entry in data:

        if entry['flag'] != '':
            continue

        sentence = entry['sentence']

        entry_id = entry['id']
        review_id = int(entry_id.split('.')[0])
        sentence_id = int(entry_id.split('.')[1])

        rate = entry['rate']

        polarity = get_polarity(sentence, rate)

        aspect = find_aspects(sentence, product_type)

        k = {}
        k['sentence'] = sentence
        k['aspects'] = aspect
        k['polarity'] = polarity
        k['id'] = entry_id

        data_to_write.append(k)

    output_file.write(make_overview_table(data_to_write))  # Write table with aspects and polarities counts

    output_file.write('\n\n\n')

    data_parsed_by_aspects = sorted(data_to_write, key=lambda k: (
        len(k['aspects']), unikey((' '.join(a for a in k['aspects']))), k['polarity'], len(k['sentence']),
        unikey(k['sentence'].lower())))

    for k in data_parsed_by_aspects:
        save_sentence(output_file, k['id'], k['sentence'], k['polarity'], k['aspects'])

    output_file.close()
