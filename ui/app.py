#!/usr/bin/env python
# Vokabelabfrager WebUI Flaskpowered

from flask import Flask, render_template
import imp
abfrager = imp.load_source('abfrager', '/Users/neo/Desktop/Vokabelabfrager/core/abfrager.py')

app = Flask("Vokabelabfrager")

@app.route("/")
def home():
	return render_template("home.html")

if __name__ == "__main__":
	app.run()