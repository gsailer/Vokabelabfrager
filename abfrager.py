#!/usr/bin/env python
# Vokabelabfrager Gabriel Sailer
import random
import sys
import argparse
import settings
import sqlite3


class Vokabel:
    abgefragt = False

    def __init__(self, vid, sprache1, sprache2):
        self.vid = vid
        self.sprache1 = sprache1
        self.sprache2 = sprache2

class Vokabelliste:
    vokabeln = []

    def __init__(self):
        self.loadData()

    def loadData(self):
        conn = sqlite3.connect(settings.database)
        c = conn.cursor()
        c.execute('SELECT VID, bedeutung1, bedeutung2 FROM data WHERE src=8')
        data = c.fetchall()
        for row in data:
            vokabel = Vokabel(row[0], row[1], row[2])
            self.vokabeln.append(vokabel)
        return 0

    def statistik(self):
        pass

    def abfrage(self):
        while True:
            ran = random.randint(0, len(self.vokabeln)-1)
            while self.vokabeln[ran].abgefragt == True:
                ran = random.randint(0, len(self.vokabeln)-1)
            print self.vokabeln[ran].sprache1
            try:
                answer = raw_input("Deutsch: ")
            except KeyboardInterrupt:
                print "\nByeBye"
                self.statistik()
                sys.exit(0)
            if answer == self.vokabeln[ran].sprache2 or answer == self.vokabeln[ran].sprache2.lower():
                print "Correct answer\n"
                self.vokabeln[ran].abgefragt = True
                continue
            else:
                while answer != self.vokabeln[ran].sprache2 or answer != self.vokabeln[ran].sprache2.lower():
                    print "Try it again"
                    try:
                        answer = raw_input("Deutsch: ")
                    except KeyboardInterrupt:
                        print "\nByeBye :)"
                        self.statistik()
                        sys.exit(0)
                    print "Well done.\n"

    def abfrageQuiz_loadData(self):
        # multiple choice with four
        # possible answers
        question = ""
        answer = ""
        options = []
        # load question+answer
        ran = random.randint(0, len(self.vokabeln)-1)
        while self.vokabeln[ran].abgefragt == True:
            ran = random.randint(0, len(self.vokabeln)-1)
        question = self.vokabeln[ran].sprache1
        answer = self.vokabeln[ran].sprache2
        # load options
        for x in xrange(0,3):
            rand = random.randint(0, len(self.vokabeln)-1)
            while rand == ran:
                rand = random.randint(0, len(self.vokabeln)-1)
            options.append(self.vokabeln[rand].sprache2)
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

    def speichern(self):
        pass

# ------ test -------
print "Vokabelabfrager"
print (len("Vokabelabfrager")*2)*"#"

vokabelnTest = Vokabelliste()
try:
    while True:
        quest, answ, opt = vokabelnTest.abfrageQuiz_loadData()
        result = vokabelnTest.abfrageQuiz(quest, answ, opt)
        if result == False:
            print "Wrong!\n"
            print 20*"-"
        else:
            print "Correct\n"
            print 20*"-"

except KeyboardInterrupt:
    vokabelnTest.statistik()
    print "\nExit."
    sys.exit(0)
