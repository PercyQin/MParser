# -*- coding: utf-8 -*-
from nltk.tree import Tree
from configReader import readStruct
strus = readStruct()

def getFatherZH(sons):
    tmps = []
    for s in sons.strip().split('\n'):
        tmps.append(s)
    print(tmps)
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


def createConstruct(ALLWord, finalX, paserList, dependency_parse):
    wordIndex = {}
    indexWord = {}
    for index, w in enumerate(ALLWord, 1):
        wordIndex[w[1]] = index
        indexWord[index] = w[1]
    print('wordIndex', wordIndex)
    print('indexWord', indexWord)
    everyWordDep = {}
    for dp in dependency_parse[1:]:
        everyWordDep[indexWord[dp[2]]] = dp[0]
    print('everyWordDep', everyWordDep)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    import re
    rmp = re.compile('\(\w+ \w+\)')
    finalTree = []
    for windex, pl in enumerate(zip(paserList), 0):
        mp = ''
        stU = pl[0].split('(')[1]
        # print(pl)
        if '.' in stU or ',' in stU or len(pl[0].strip()) <= 5:
            print(pl, '******')
            finalTree.append(str(pl)[2:-3])
        else:
            mp = stU.strip()
        nnWordList = rmp.findall(str(pl))
        for index, nw in enumerate(nnWordList, 1):
            tnw = nw.strip('(').strip(')').split()
            cixing = tnw[0]
            word = tnw[1]
            # print(mp, cixing, word)
            if mp in strus.keys():
                for one in strus[mp]:

                    # print(one, mp, 'XXXX')
                    if one[-1] == '0':
                        if one[0].strip() == '':
                            print(mp, '>>>', one[1], 111)
                            finalTree.append(re.sub(mp, one[1], str(pl))[2:-3])
                            break
                        else:
                            if one[0].strip() == everyWordDep[word]:
                                print(mp, '>>>', one[1], 222)
                                finalTree.append(re.sub(mp, one[1], str(pl))[2:-3])
                                break
                            else:
                                pass
                    elif one[-1] == finalX[mp+' _{}'.format(windex)].strip():
                        if one[0].strip() == '':
                            print(mp, '>>>', one[1], 333)
                            finalTree.append(re.sub(mp, one[1], str(pl))[2:-3])
                            break
                        else:
                            if one[0].strip() == everyWordDep[word]:
                                print(mp, '>>>', one[1], 444)
                                finalTree.append(re.sub(mp, one[1], str(pl))[2:-3])
                                break
                            else:
                                pass
            else:
                print('不在梳理的结构内，请重试...')
    # print('MMMMMMMMMMMMMMMMMMMMMM')
    for l in finalTree:
        print(str(l))
    return ''.join(finalTree), finalTree

if __name__ == '__main__':
    ALLWord = [('NN', 'apple'), ('VBZ', 'is'), ('VBN', 'push'), ('IN', 'by'), ('NN', 'post'), ('.', '.')]
    upt_pos_word = [('apple', 'ncm'), ('push', 'vtr'), ('is', 'null'), ('by', 'prep'), ('post', 'ncm')]
    constructInfo = [('apple', 'ncm', '0x5107df000eae', '0'), ('push', 'vtr', '0x5707df003737', '42'),
                     ('by', 'prep', '0x5a07df000321', ''), ('post', 'ncm', '0x5107df02c33e', '0')]
    sons = '''(ROOT
  (S
    (NP (NN apple))
    (VP (VBZ is)
      (VP (VBN push)
        (PP (IN by)
          (NP (NN post)))))
    (. .)))


    '''
    dependency_parse = [('ROOT', 0, 3), ('nsubj', 3, 1), ('cop', 3, 2), ('case', 5, 4), ('nmod', 3, 5), ('punct', 3, 6)]
    finalX, paserList = getFatherZH(sons)
    print('finalX', finalX)
    print('paserList', paserList)
    drawTree, str_draw = createConstruct(ALLWord, finalX, paserList, dependency_parse)
    Tree.fromstring(drawTree).draw()

