#!/usr/bin/env python
# Vokabelabfrager Gabriel Sailer
import random
import sys
import argparse
import sqlite3
import imp

if __name__ == "__main__":
    settings = imp.load_source('settings','./settings.py')
else:
    settings = imp.load_source('settings', '../core/settings.py')

class Vokabel:
    abgefragt = False

    def __init__(self, vid, sprache1, sprache2, liste):
        self.vid = vid
        self.sprache1 = sprache1
        self.sprache2 = sprache2
        self.liste = liste

class Vokabelliste:
    vokabeln = []

    def __init__(self):
        self.loadData()

    def loadData(self):
        conn = sqlite3.connect(settings.database)
        c = conn.cursor()
        c.execute('SELECT VID, bedeutung1, bedeutung2, src FROM data')
        data = c.fetchall()
        for row in data:
            vokabel = Vokabel(row[0], row[1], row[2], row[3])
            self.vokabeln.append(vokabel)
        return 0

    def getVokabelByList(self, liste):
        newlist = []
        for vocab in self.vokabeln:
            if vocab.liste == liste:
                newlist.append(vocab)
        return newlist, len(newlist)

    def getFiles(self):
        conn = sqlite3.connect(settings.database)
        c = conn.cursor()
        c.execute('SELECT filename FROM files;')
        files_raw = c.fetchall()
        files = []
        for file in files_raw:
            fl = file[0]
            fl = fl[3:-4]
            files.append(fl)
        return files

    def statistik(self):
        pass

    def abfrageQuiz_loadData(self, list, vokabelindex):
        # multiple choice with four
        # possible answers
        vokabelnByList, _ = self.getVokabelByList(list)
        question = vokabelnByList[vokabelindex].sprache1
        answer = vokabelnByList[vokabelindex].sprache2
        options = []
    
        # load options
        for x in xrange(0,3):
            ran = random.randint(0, len(vokabelnByList)-1)
            while ran == vokabelindex:
                ran = random.randint(0, len(vokabelnByList)-1)
            options.append(vokabelnByList[ran].sprache2)
        options.append(answer)
        random.shuffle(options)
        # returns: question string, answer string, options array[str]
        return question, answer, options

    def abfrageQuiz(self, question, answer, options):
        # actual function for multi choice
        print question + "\n"
        a = 0
        for i in options:
            print str(a) + ") " + i + "\n"
            a = a+1

        ans = input("Which one is right? ")
        if ans > len(options)+1 or ans < 0:
            print "Error: vocabulary not in range"
            ans =  input("please try again: ")
        if options[ans] == answer:
            return True
        else:
            return False