# Kludge to be able to sort Portuguese words alphabetically.
s = 'aáÁàÀAâÂbBcCçÇdDeêÊéEfFgGğĞhHiİîÎíīıIÍjJkKlLmMnNóoOÓöÖôpPqQrRsSşŞtTuUÚûúÛüÜvVwWxXyYzZ_'
s2 = 'aaaaaaaabbccccddeeeeeffgggghhiiiiiiiiijjkkllmmnnooooooÔppqqrrssssttuuuuuuuuvvwwxxyyzzz'
trans = str.maketrans(s, s2)


def unikey(seq):
    if '_' in seq:  # Specific for the aspect '_TOTAL_', which goes in the last line of the table.
        return 'zzzzzzzzzz'
    return seq.translate(trans)


def make_overview_table(data_to_write):
    list_of_aspects = count_aspects(data_to_write)
    s = '# '
    s += "%-17s" % 'aspects'
    s += "%10s" % 'positive'
    s += "%10s" % 'negative'
    s += "%10s" % 'neutral'
    s += "%10s" % 'non-op'
    s += "%10s" % 'total'
    s += "%10s" % 'exclus'
    s = s.replace(' ', '_')
    s += '\n'
    for a in sorted(list_of_aspects, key=unikey):
        s += '# '
        l = aspect_stats(list_of_aspects, a)
        if len(s.splitlines()) % 2 == 1:
            l = l.replace('   ', ' _ ')
        if a == '_TOTAL_':
            l = l.replace(' ', '_')
        s += l
        s += '\n'
    return s


def count_aspects(info):
    count_aspects = {}
    count_aspects['_TOTAL_'] = {'+': 0, '-': 0, '.': 0, 'x': 0, 'total': 0, 'exc': 0}
    for i in info:
        for asp in i['aspects']:
            if asp not in count_aspects:
                count_aspects[asp] = {'+': 0, '-': 0, '.': 0, 'x': 0, 'total': 0, 'exc': 0}
            count_aspects[asp][(i['polarity'])] += 1
            count_aspects['_TOTAL_'][(i['polarity'])] += 1

            if len(i['aspects']) == 1:
                count_aspects[asp]['exc'] += 1
                count_aspects['_TOTAL_']['exc'] += 1

    return count_aspects


def aspect_stats(list_of_aspects, aspect):
    s = ''
    s += "%-21s" % (aspect)
    s += "%6d" % list_of_aspects[aspect]['+']
    s += "%10d" % list_of_aspects[aspect]['-']
    s += "%10d" % list_of_aspects[aspect]['.']
    s += "%10d" % list_of_aspects[aspect]['x']
    s += "%10d" % (list_of_aspects[aspect]['+'] + list_of_aspects[aspect]['-'] + list_of_aspects[aspect]['.'] + list_of_aspects[aspect]['x'])
    s += "%10d" % (list_of_aspects[aspect]['exc'])
    return s.replace(' 0 ', '   ')
