import json
import pprint

aspects = json.loads(open("aspects.json", 'r').read())
b = open("aspects_bck.json", 'w')
b.write(pprint.pformat(aspects).replace('\'', '\"'))
b.close()

for t in dict(aspects):
    for i in dict(aspects[t]):
        if t == 'GENERIC':
            continue
        if i in aspects['GENERIC'] and aspects['GENERIC'][i] == aspects[t][i]:
            print('deleting  ', t, i, aspects[t][i])
            del aspects[t][i]

a = pprint.pformat(aspects)

s = open("aspects.json", 'w')
s.write(a.replace('\'', '\"'))

s.close()
