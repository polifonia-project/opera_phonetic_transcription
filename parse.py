import collections
import csv


def split_arpa_phonemes(arpa):
    splitted_word = []
    print(arpa)
    while arpa != '':
        if arpa.startswith('LH'):
            arpa = arpa.replace('LH', 'LY', 1)
        if arpa.startswith('GN'):
            arpa = arpa.replace('GN', 'NY', 1)
        candidates = [aphon for aphon in arpabet_phonemes if arpa.startswith(aphon)]
        lengths = [len(c) for c in candidates]
        try:
            aphone = candidates[lengths.index(max(lengths))]
        except:
            if arpa.startswith('OH'):
                arpa = arpa.replace('OH','OW',1)
                continue
            if arpa.startswith('H'):
                arpa = arpa.replace('H','HH',1)
                continue
            print('----ERROR-----', arpa)
            return '----ERROR-----'
        splitted_word.append(aphone)
        arpa = arpa.replace(aphone,'',1)
    return ' '.join(splitted_word)

with open('data/arpabet.tsv') as f:
    reader = csv.reader(f, delimiter='\t')
    arpabet_phonemes = [r[0] for r in reader]

for aria in ['trovatore', 'rigoletto', 'norma']:
    phon = {}
    arpabet = {}
    transcription = {}
    with open('data/' + aria +'_phon') as f:
        lines = f.readlines()

    for line in lines:
        tokens = line.split()
        if len(tokens)>0:
            first = tokens[0]
            if first.isnumeric():
                if first not in phon:
                    phon[first] = tokens
                else:
                    arpabet[first] = tokens
    for k, v in phon.items():
        phonetic = arpabet[k]
        for word, arpa in zip(v, phonetic):
            if not word.isnumeric() and not arpa.isnumeric() and arpa not in ['!','?', '.', ',', ';', ':', '-']:
                arpa = arpa.replace('1','').replace('_','')
                arpa_ = split_arpa_phonemes(arpa)
                print(word.split('/')[0], arpa)
                if arpa_ == '----ERROR-----':
                    transcription[word.split('/')[0].lower()] = arpa + '-----> ERROR'
                else:
                    transcription[word.split('/')[0].lower()] = arpa_

    ordered = collections.OrderedDict(sorted(transcription.items()))

    with open('data/' + aria + '_transcription.tsv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for k, v in ordered.items():
            writer.writerow([k,v])