#!/usr/bin/env python
# Vokabelabfrager WebUI Flaskpowered

from flask import Flask, render_template, jsonify
import imp
abfrager = imp.load_source('abfrager', '../core/abfrager.py')

app = Flask("Vokabelabfrager")
cache = abfrager.Vokabelliste()
@app.route("/")
def home():
	file = cache.getFiles()
	return render_template("home.html", files = file)

@app.route("/quiz/<file>")
def abfrage(file):
	return render_template("abfrage.html")

###### API #####
@app.route("/api/vokabellists")
def vokabellists():
	return jsonify(list = cache.getFiles())

@app.route("/api/vokabelset/<int:list>", methods=['GET'])
def vokabeldata(list):
	data = []
	_, count = cache.getVokabelByList(list)
	for iter in xrange(count):
		i = cache.abfrageQuiz_loadData(list, iter)
		data.append(i)
	return jsonify(vokabelset = data)

if __name__ == "__main__":
	app.run(host="172.24.41.167", port=80) # port 80 requires sudo
