# -*- coding: utf-8 -*-
from operator import itemgetter, attrgetter

def readConfig(filename):
    '''
    :param filename:
    :return:
    '''
    datas = {}

    with open(filename) as fr:
        fr.readline()
        for line in fr:
            newline = line.strip().split('\t')
            datas[newline[0].strip()] = newline[1].strip()
    return datas

def getInfo(filename):
    id2pos = {}
    id2word = {}
    word2id = {}
    id2text = {}
    word2pos = {}
    with open(filename, encoding='utf-8') as fr:
        for line in fr:
            newline = line.strip().split('|')
            id_ = newline[1]
            pos = newline[0]
            word = newline[2]
            text = newline[3]

            id2pos[id_] = pos
            id2word[id_] = word
            id2text[id_] = text

            word2id.setdefault(word, []).append([id_, word, pos, text])
            word2pos.setdefault(word, []).append([id_, word, pos, text])

    return id2pos, id2word, id2text, word2id, word2pos

def readPosId():
    posInsPos = []
    with open('./config/map_pos.txt', encoding='utf-8') as fr:
        for line in fr:
            nl = line.strip().split('\t')
            assert len(nl) == 4
            posInsPos.append(nl)
    return posInsPos

def readStruct():
    construct = {}
    with open('./config/en_construct.txt', encoding='utf-8') as fr:
        fr.readline()
        for line in fr:
            newline = line.strip().split('\t')
            assert len(newline) == 4
            construct.setdefault(newline[0], []).append(newline[1:])
    tmps = {}
    for k, v in construct.items():
        tmps[k] = sorted(v, key=itemgetter(2, 0), reverse=True)
        # print(k, sorted(v, key=itemgetter(2, 0), reverse=True))
    return tmps
if __name__ == '__main__':
    posInsPos = readStruct()
    print(posInsPos)
