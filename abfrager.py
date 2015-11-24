#!/usr/bin/env python
# Vokabelabfrager Gabriel Sailer
# First Version - Sept 2015
import csv, random, sys

def loadCSV(table, liste):
	with open(table, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=';')
		for item in reader:
			vokabel = Vokabel(item[0], item[1])
			liste.append(vokabel)
	return 0

class Vokabel:
	anzahl_abfragen = 0
	gewusst = False

	def __init__(self, sprache1, sprache2):
		self.sprache1 = sprache1
		self.sprache2 = sprache2

class Vokabelliste:
	vokabeln = []

	def __init__(self, table):
		loadCSV(table, self.vokabeln)

	def statistik(self):
		gesamt = len(self.vokabeln)
		abgefragt = 0
		korrekt = 0
		for x in self.vokabeln: 
			if x.anzahl_abfragen > 0:
				abgefragt +=1
				if x.gewusst:
					korrekt += 1
		korrekt_prozent = (abgefragt/korrekt)*100

		print "--------------------------------------"
		print "Statistik"
		print "Vokabeln geladen: %s" %gesamt
		print "Vokabeln abgefragt: %s" %abgefragt
		print "Anteil Vokabeln korrekt: %s Prozent" %korrekt_prozent

	def abfragen(self):
		while True:
			ran = random.randint(0,len(self.vokabeln)-1)
			while self.vokabeln[ran].gewusst == True:
				ran = random.randint(0, len(self.vokabeln)-1)
			print self.vokabeln[ran].sprache1
			try:
				answer = raw_input("Deutsch: ")
			except KeyboardInterrupt:
				print "\nByeBye :)"
				self.statistik()
				sys.exit(0)
			if answer == self.vokabeln[ran].sprache2 or answer == self.vokabeln[ran].sprache2.lower():
				print "Correct answer :)\n"
				self.vokabeln[ran].gewusst = True
				self.vokabeln[ran].anzahl_abfragen += 1
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

					
	def speichern():
		pass

# ------ test -------
print "Vokabelabfrager"
print (len("Vokabelabfrager")*2)*"#"

liste = raw_input("Welche Vokabelliste willst du beutzen?\n")
vokabelnTest = Vokabelliste(liste)
vokabelnTest.abfragen()