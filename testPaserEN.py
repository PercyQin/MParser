# -*- coding: utf-8 -*-
import os
import re
def write2fox(pos_word_list):
    fw = open('fox.txt', 'w')
    tmp = []
    for i in pos_word_list:
        tmp.append('/'.join([i[1], i[0]]))
    fw.write(' '.join(tmp))
    fw.flush()
    fw.close()
    print('OK')

def getPase(stf_paser, user_input):

    commend = 'java -mx1g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -tokenized -tagSeparator / -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz fox.txt'
    nlpread = os.popen(commend).read()
    print(nlpread)
    # Tree.fromstring(nlpread).draw()

    for up in user_input:
        tmp = up[1] + ' ' + up[0]
        for stfp in stf_paser:
            if up[0] == stfp[1]:
                print(' '.join(stfp), tmp)
                nlpread = re.sub(' '.join(stfp), tmp, nlpread)
    return nlpread
if __name__ == '__main__':
    from nltk import Tree
    stf_paser = [('NN', 'apple'), ('POS', "'s"), ('NNS', 'friend'), ('VBP', 'have'), ('VBN', 'finish'), ('NN', 'homework'), (',', ',')]
    user_input = [('apple', 'ncm'), ("'s", 'par'), ('friend', 'ncm'), ('finish', 'vtr'), ('have', 'null'), ('homework', 'ncm')]
    write2fox(stf_paser)
    nlpread = getPase(stf_paser, user_input)
    print(nlpread)
