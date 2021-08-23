# -*- coding: utf-8 -*-
# @Author  : Percy Qin
import os
from nltk.tree import Tree
from configReader import readConfig, getInfo, readPosId

mc_data = readConfig('./config/mc.txt')
dc_data = readConfig('./config/dc.txt')
posInsPos = readPosId()

en_id2pos, en_id2word, en_id2text, en_word2id, en_word2pos = getInfo('./data/Vocabulary_en.txt')
# zh_id2pos, zh_id2word, zh_id2text, zh_word2id, zh_word2pos = getInfo('./data/Vocabulary_zh.txt')

def getPase():

    commend = 'java -mx1g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -tokenized -tagSeparator / -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz fox.txt'
    nlpread = os.popen(commend).read()
    print(nlpread)
    Tree.fromstring(nlpread).draw()

    print('>>>>>>>>>>>>>>;c r>>>>>>>>>>>>>>>>>>>>>>')
# getPase()

def main():
    ALLWord = []
    constructInfo = []
    u_input = input('请输入词数：')
    upt_pos_word = []
    for u in range(int(u_input)):
        u_datas = []
        tmpWord = []
        word = input('输入词:')
        word = word.strip()
        if word in [',', '.', '!', '?']:
            if word == ',':
                ALLWord.append(('%s' % word, '%s' % word))
            else:
                ALLWord.append(('.', '.'))
            continue
        if word.strip() not in en_word2pos.keys():
            print('该词不在语料库中！！！')
            continue
        else:
            tmp = {}
            for index, i in enumerate(en_word2pos[word], 1):
                tmp[index] = i
                print('\t', index, i)
            chose = input('选择序号：')
            print('你的选择是:{}, {}'.format(chose, tmp[int(chose)][2]))
            pos_final = tmp[int(chose)][2]
            upt_pos_word.append((word, pos_final))
            u_datas.append((word, tmp[int(chose)][0], tmp[int(chose)][2]))
            if tmp[int(chose)][2] in ['vtr', 'vit', 'vdi']:
                tmp2 = {}
                for index, (k, v) in enumerate(dc_data.items(), 1):
                    tmp2[index] = (k, v)
                    print('\t', index, k, v)
                chose2 = input('选择是动词，再次选择序号：')
                isn = tmp2[int(chose2)][1]
                print('你的选择是:{}, {}'.format(chose2, isn))
                u_datas.append((word, tmp[int(chose)][0], tmp[int(chose)][2]))
                for m in posInsPos:
                    if m[1] != '':
                        if u_datas[0][1] == m[1] and u_datas[0][2] == m[0]:
                            pos_final = m[-1]
                            tmpWord.append((pos_final, word))
                        else:
                            pass
                    elif m[2] != '':
                        if isn == m[2] and u_datas[0][2] == m[0]:
                            pos_final = m[-1].split('+')[-1].strip()
                            dlt = m[-1].split('+')[:-1]
                            for d_ in dlt:
                                dd = d_.strip().strip('()').split()
                                if len(dd) == 1:
                                    pass
                                else:
                                    upt_pos_word.append((dd[0], 'null'))
                                    tmpWord.append((dd[-1], dd[0]))
                            tmpWord.append((pos_final, word))
                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                    else:
                        pass
                print([x for x in tmpWord if len(x) > 0], 'VVVVVVVVVVVVVV')
                ALLWord.extend([x for x in tmpWord if len(x) > 0])
            elif tmp[int(chose)][2] in ['ncm', 'npp', 'ntp']:
                tmp2 = {}
                for index, (k, v) in enumerate(mc_data.items(), 1):
                    tmp2[index] = (k, v)
                    print('\t', index, k, v)
                chose2 = input('选择是名词，再次选择序号：')
                isn = tmp2[int(chose2)][1]
                print('你的选择是:{}, {}'.format(chose2, isn))
                for m in posInsPos:
                    if m[1] != '':
                        if u_datas[0][1] == m[1] and u_datas[0][2] == m[0]:
                            pos_final = m[-1]
                            tmpWord.append((pos_final, word))
                        else:
                            pass
                    elif m[2] != '':
                        if isn == m[2] and u_datas[0][2] == m[0]:
                            pos_final = m[-1].split('+')[-1].strip()
                            dlt = m[-1].split('+')[:-1]
                            for d_ in dlt:
                                dd = d_.strip().strip('()').split()
                                if len(dd) == 1:
                                    pass
                                else:
                                    upt_pos_word.append((dd[0], 'null'))
                                    tmpWord.append((dd[-1], dd[0]))
                            tmpWord.append((pos_final, word))
                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                    else:
                        pass
                print([x for x in tmpWord if len(x) > 0], 'MMMMMMMMMMMMMMM')
                ALLWord.extend([x for x in tmpWord if len(x) > 0])
            else:
                print('>>>>>>>>>>>>>>>>', u_datas)
                for m in posInsPos:
                    if m[1] != '':
                        if u_datas[0][1] == m[1] and u_datas[0][2] == m[0]:
                            pos_final = m[-1]
                            tmpWord.append((pos_final, word))
                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                    else:
                        pass
                ALLWord.extend(tmpWord)
        if len(tmpWord) == 0:
            ALLWord.extend((pos_final, word))
    print(ALLWord)
    print(upt_pos_word)
    return ALLWord, upt_pos_word
from testPaser import *
stf_paser, user_input = main()
write2fox(stf_paser)
getPase(stf_paser, user_input)
print('开始画结构信息...')
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
    (. .)))'''
dependency_parse = [('ROOT', 0, 3), ('nsubj', 3, 1), ('cop', 3, 2), ('case', 5, 4), ('nmod', 3, 5), ('punct', 3, 6)]
finalX, paserList = getFather(sons)
print('finalX', finalX)
print('paserList', paserList)
drawTree, str_draw = createConstruct(ALLWord, finalX, paserList, dependency_parse)
Tree.fromstring(drawTree).draw()