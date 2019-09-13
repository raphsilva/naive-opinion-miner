negative_clues = ['poderia',
                  'deveria',
                  'odiei',
                  'não gostei',
                  'a desejar',
                  'ruim',
                  'péssimo',
                  'complicado',
                  'difícil',
                  'feio',
                  'lixo']

max_rate = 5


def rate_to_polarity(rate):
    if rate / max_rate > 0.5:
        return '+'
    elif rate / max_rate < 0.5:
        return '-'
    else:
        return '.'


def get_polarity(text, rate):
    p = rate_to_polarity(rate)

    for i in negative_clues:
        if i in text.lower():
            p = '-'
    return p
