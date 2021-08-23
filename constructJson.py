# -*- coding: utf-8 -*-
from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'./')

sentence = " 使变成 雌性 ."
print(nlp.parse(sentence))
print(nlp.dependency_parse(sentence))
from nltk.tree import Tree

Tree.fromstring(nlp.parse(sentence)).draw()
