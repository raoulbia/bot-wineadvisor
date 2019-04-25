#!/usr/bin/env python3

# from nltk.parse import CoreNLPParser
# from nltk.parse.corenlp import CoreNLPDependencyParser

parser = CoreNLPParser(url='http://188.166.145.126:9000')
dep_parser = CoreNLPDependencyParser(url='http://188.166.145.126:9000')

text = 'What is the airspeed of an unladen swallow ?'
text = 'I want to drink wine for dinner'
# parser
# print(list(parser.parse(text.split())))


# dependency parser
iter = dep_parser.parse(text.split())
dep = next(iter)

print(list(dep.tree()))

for t in dep.triples():
    print(t)

dep.tree().draw()