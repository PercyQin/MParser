# -*- coding: utf-8 -*-
# @Author  : percy qin
import os
from nltk.tree import Tree
from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'./',lang="zh")
from configReaderZH import readConfig, getInfo, readPosId
from testPaserZH import write2fox, getPase
from pase2textUpZH import getFatherZH, createConstruct
from create2sentenceZH import *

mc_data = readConfig('./config/mc.txt')
dc_data = readConfig('./config/dc.txt')
posInsPos = readPosId()

en_id2pos, en_id2word, en_id2text, en_word2id, en_word2pos = getInfo('./data/Vocabulary_en.txt')
zh_id2pos, zh_id2word, zh_id2text, zh_word2id, zh_word2pos = getInfo('./data/Vocabulary_zh.txt')

def main():
    ALLWord = []
    constructInfo = []
    upt_pos_word = []
    while True:
        u_datas = []
        tmpWord = []
        word = input('Input words:').strip()
        if word == 'end':
            break


        if word in [',', '.', '!', '?']:
            if word == ',':
                ALLWord.append(('%s' % word, '%s' % word))
            else:
                ALLWord.append(('.', '.'))
            continue
        if word.strip() not in zh_word2pos.keys():
            print('Sorry, No the word in our Codic, Again!')
            continue
        else:
            tmp = {}
            for index, i in enumerate(zh_word2pos[word], 1):
                tmp[index] = i
                print('\t', index, i)
            chose = input('Choose word No.：')
            print('You choose***:{}, {}'.format(chose, tmp[int(chose)][2]))
            pos_final = tmp[int(chose)][2]
            iid = tmp[int(chose)][0]

            upt_pos_word.append((word, pos_final))
            u_datas.append((word, tmp[int(chose)][0], tmp[int(chose)][2]))

            if tmp[int(chose)][2] in ['vtr', 'vit', 'vdi']:
                tmp2 = {}
                for index, (k, v) in enumerate(dc_data.items(), 1):
                    tmp2[index] = (k, v)
                    print('\t', index, k, v)
                chose2 = input('Verb，Next choose：')
                isn = tmp2[int(chose2)][1]
                print('You choose:{}, {}'.format(chose2, isn))
                u_datas.append((word, tmp[int(chose)][0], tmp[int(chose)][2]))
                for m in posInsPos:
                    if m[1] != '':
                        if u_datas[0][1] == m[1] and u_datas[0][2] == m[0]:
                            pos_final = m[-1]
                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, ''))
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
                                    #constructInfo.append((dd[0], 'null', iid, isn))
                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, isn))
                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                        constructInfo.append((word, tmp[int(chose)][2], iid, ''))
                    else:
                        pass
                print([x for x in tmpWord if len(x) > 0], 'VVVVVVVVVVVVVV')
                ALLWord.extend([x for x in tmpWord if len(x) > 0])
            elif tmp[int(chose)][2] in ['ncm', 'npp', 'ntp']:
                tmp2 = {}
                for index, (k, v) in enumerate(mc_data.items(), 1):
                    tmp2[index] = (k, v)
                    print('\t', index, k, v)
                chose2 = input('Noun，Next choose：')
                isn = tmp2[int(chose2)][1]
                print('You choose:{}, {}'.format(chose2, isn))
                for m in posInsPos:
                    if m[1] != '':
                        if u_datas[0][1] == m[1] and u_datas[0][2] == m[0]:
                            pos_final = m[-1]
                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, ''))
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
                                    constructInfo.append((word, tmp[int(chose)][2], iid, isn))

                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, isn))
                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                        constructInfo.append((word, tmp[int(chose)][2], iid, ''))

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
                            constructInfo.append((word, tmp[int(chose)][2], iid, ''))

                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                        constructInfo.append((word, tmp[int(chose)][2], iid, ''))
                    else:
                        pass
                ALLWord.extend(tmpWord)
        if len(tmpWord) == 0:
            ALLWord.extend((pos_final, word))
            constructInfo.append((word, tmp[int(chose)][2], iid, ''))

    print('ALLWord', ALLWord)
    print('upt_pos_word', upt_pos_word)
    print('constructInfo', constructInfo)
    return ALLWord, upt_pos_word, constructInfo

def main2():
    ALLWord = []
    constructInfo = []
    upt_pos_word = []
    while True:
        u_datas = []
        tmpWord = []
        word = input('Input words:').strip()
        if word == 'end':
            break


        if word in [',', '.', '!', '?']:
            if word == ',':
                ALLWord.append(('%s' % word, '%s' % word))
            else:
                ALLWord.append(('.', '.'))
            continue
        if word.strip() not in zh_word2pos.keys():
            print('Sorry, No the word in our Codic, Again! ！！！')
            continue
        else:
            tmp = {}
            for index, i in enumerate(zh_word2pos[word], 1):
                tmp[index] = i
                print('\t', index, i)
            chose = input('Choose word No.：')
            print('You choose***:{}, {}'.format(chose, tmp[int(chose)][2]))
            pos_final = tmp[int(chose)][2]
            iid = tmp[int(chose)][0]

            upt_pos_word.append((word, pos_final))
            u_datas.append((word, tmp[int(chose)][0], tmp[int(chose)][2]))

            if tmp[int(chose)][2] in ['vtr', 'vit', 'vdi']:
                tmp2 = {}
                for index, (k, v) in enumerate(dc_data.items(), 1):
                    tmp2[index] = (k, v)
                    print('\t', index, k, v)
                chose2 = input('Verb，Next choose：')
                isn = tmp2[int(chose2)][1]
                print('You choose:{}, {}'.format(chose2, isn))
                u_datas.append((word, tmp[int(chose)][0], tmp[int(chose)][2]))
                for m in posInsPos:
                    if m[1] != '':
                        if u_datas[0][1] == m[1] and u_datas[0][2] == m[0]:
                            pos_final = m[-1]
                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, ''))
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
                                    #constructInfo.append((dd[0], 'null', iid, isn))
                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, isn))
                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                        constructInfo.append((word, tmp[int(chose)][2], iid, ''))
                    else:
                        pass
                print([x for x in tmpWord if len(x) > 0], 'VVVVVVVVVVVVVV')
                ALLWord.extend([x for x in tmpWord if len(x) > 0])
            elif tmp[int(chose)][2] in ['ncm', 'npp', 'ntp']:
                tmp2 = {}
                for index, (k, v) in enumerate(mc_data.items(), 1):
                    tmp2[index] = (k, v)
                    print('\t', index, k, v)
                chose2 = input('Noun，Next choose：')
                isn = tmp2[int(chose2)][1]
                print('You choose:{}, {}'.format(chose2, isn))
                for m in posInsPos:
                    if m[1] != '':
                        if u_datas[0][1] == m[1] and u_datas[0][2] == m[0]:
                            pos_final = m[-1]
                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, ''))
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
                                    constructInfo.append((word, tmp[int(chose)][2], iid, isn))

                            tmpWord.append((pos_final, word))
                            constructInfo.append((word, tmp[int(chose)][2], iid, isn))
                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                        constructInfo.append((word, tmp[int(chose)][2], iid, ''))

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
                            constructInfo.append((word, tmp[int(chose)][2], iid, ''))

                        else:
                            pass
                    elif m[1] == m[2] and u_datas[0][2] == m[0]:
                        pos_final = m[-1]
                        tmpWord.append((pos_final, word))
                        constructInfo.append((word, tmp[int(chose)][2], iid, ''))
                    else:
                        pass
                ALLWord.extend(tmpWord)
        if len(tmpWord) == 0:
            ALLWord.extend((pos_final, word))
            constructInfo.append((word, tmp[int(chose)][2], iid, ''))

    print('ALLWord', ALLWord)
    print('upt_pos_word', upt_pos_word)
    print('constructInfo', constructInfo)
    return ALLWord, upt_pos_word, constructInfo

def enRun(ALLWord, upt_pos_word, constructInfo):
    write2fox(ALLWord)
    nlpread = getPase(ALLWord, upt_pos_word)

    print('替换结构结构中...')
    sentence = ' '.join([x[1] for x in ALLWord])

    print(sentence)
    dependency_parse = nlp.dependency_parse(sentence)
    print('dependency_parse', dependency_parse)

    finalX, paserList = getFather(nlpread)
    print('finalX', finalX)
    print('paserList', paserList)
    drawTree, str_draw = createConstruct(ALLWord, finalX, paserList, dependency_parse)
    Tree.fromstring(drawTree).draw()

    print('开始构建句子...')
    en_, zh_ = createSentence(upt_pos_word, constructInfo, str_draw)
    print(en_)
    print('开始进行翻译...')
    print(zh_)

def zhRun(ALLWord, upt_pos_word, constructInfo):
    write2fox(ALLWord)
    nlpread = getPase(ALLWord, upt_pos_word)

    print('Structure building...')
    sentence = ' '.join([x[1] for x in ALLWord])

    print(sentence)
    dependency_parse = nlp.dependency_parse(sentence)
    print('dependency_parse', dependency_parse)

    finalX, paserList = getFatherZH(nlpread)
    print('finalX', finalX)
    print('paserList', paserList)
    drawTree, str_draw = createConstruct(ALLWord, finalX, paserList, dependency_parse)
    Tree.fromstring(drawTree).draw()

    print('Sentence generation...')
    zh_, en_ = createSentence(upt_pos_word, constructInfo, str_draw)
    print(zh_)
    print('Mapping to English...')
    print(en_)
    print('Finished')


if __name__ == '__main__':
    while True:
        a = input('Choose Language：0 English， 1 Chinese：')
        if a == '0':
            print('ENGLISH！！！')
            ALLWord, upt_pos_word, constructInfo = main()
        if a == '1':
            print('CHINESE！！！')
            ALLWord, upt_pos_word, constructInfo = main2()
            zhRun(ALLWord, upt_pos_word, constructInfo)
