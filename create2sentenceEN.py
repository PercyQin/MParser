# -*- coding: utf-8 -*-
import re

from configReader import getInfo
zh_id2pos, zh_id2word, zh_id2text, zh_word2id, zh_word2pos = getInfo('./data/Vocabulary_zh.txt')

def getFatherRun(sons):
    tmps = []
    for s in sons:
        tmps.append(s)
    # print(tmps)
    lens = [len(x.split('(')[0]) for x in tmps if '.' not in x]
    # print(lens)
    pascoms = [x.split('(')[1] for x in tmps if '.' not in x]
    # print([x.split('(')[1] for x in tmps if '.' not in x])
    son2father = {}
    for aindex, a in enumerate(lens):
        for bindex, b in enumerate(lens):
            if b - a == 2:
                son2father[bindex] = aindex
            else:
                pass
    # print(son2father)
    finalX = {}
    for k, v in son2father.items():
        kk = pascoms[k]
        vv = pascoms[v]
        finalX[kk +'_'+str(k)] = vv
    return finalX, tmps

def createSentence(upt_pos_word, constructInfo, sons):
    # print('sons', sons)
    ukeys = [x[0] for x in upt_pos_word if x[1] != 'null']
    a, b = getFatherRun(sons)
    tmps = []
    recp = re.compile('\(\w+ \w+\)')
    index2word = {}
    word2struct = {}
    for i in b[1:]:
        if '(S' in i:
            tmps.append('S.0.0')
        elif ',' in i or '.' in i or 'null' in str(i):
            continue
        else:
            # print(i, i.index('('))
            stru_word = i.strip().split()[0][1:]
            for pos_word in recp.findall(i):
                pos, word = pos_word[1:-1].split(' ')
                index2word[word] = i.index('(')
                word2struct[word] = stru_word
                # print(pos, word, i.index('('))
    min_index = min(list(index2word.values()))
    # print('min_index', min_index)
    final_index_word = {}
    for k, v in index2word.items():
        if k in ukeys:
            if v - min_index == 0:
                # print(k, v, min_index, v - min_index)
                final_index_word[k] = 1
            else:
                # print(k, v, min_index, v - min_index)
                final_index_word[k] = int(((v - min_index) / 2) + 1)

    # print(final_index_word)
    # print(word2struct)
    final_sentence = []
    final_sentence.append('S.0.0')
    fanyi_results = []
    for w in constructInfo:
        word = w[0]
        iid = w[2]
        ins = w[3]
        constru = word2struct[word]
        father_son = str(final_index_word[word]-1)+'.'+str(final_index_word[word])
        if ins == '':
            sents = '.'.join([word, iid, constru, father_son])
            try:
                fanyi_results.append(zh_id2word[iid])
            except:
                pass
        else:
            sents = '.'.join([word, iid, ins, constru, father_son])
            try:
                fanyi_results.append(zh_id2word[iid])
            except:
                pass
        final_sentence.append(sents)
    ends = [')'] * len(final_index_word.keys())
    return '('.join(final_sentence) + ''.join(ends), ''.join(fanyi_results)

if __name__ == '__main__':
    upt_pos_word = [('apple', 'ncm'), ('push', 'vtr'), ('is', 'null'), ('by', 'prep'), ('post', 'ncm')]
    constructInfo = [('apple', 'ncm', '0x5107df000eae', '0'), ('push', 'vtr', '0x5707df003737', '42'),
                     ('by', 'prep', '0x5a07df000321', ''), ('post', 'ncm', '0x5107df02c33e', '0')]
    sons = '''(ROOT
                      (S
                        (A (ncm apple))
                        (P (null is)
                          (P (vtr push)
                            (Cv (prep by)
                              (N (ncm post)))))
                        (. .)))'''
    en_, zh_ = createSentence(upt_pos_word, constructInfo, sons)
    print(en_)
    print(zh_)