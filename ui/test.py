#!/usr/bin/env python
# test.py
import imp
abfrager = imp.load_source('abfrager', '../core/abfrager.py')

test = abfrager.Vokabelliste()
print test.abfrageQuiz_loadData(1,1)