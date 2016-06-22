#!/usr/bin/env python
# Vokabel Import
import csv
import sqlite3
import settings
import glob
import sys
from datetime import date

date = str(date.today())


def connectDB(database):
    return sqlite3.connect(database)


def createTables(conn):
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS data(VID INTEGER PRIMARY KEY AUTOINCREMENT, bedeutung1 TEXT,bedeutung2 TEXT, src INTEGER)')
    c.execute(
        'CREATE TABLE IF NOT EXISTS stats(level INTEGER, anzahl_abfragen INTEGER, vokabel INTEGER)')
    c.execute(
        'CREATE TABLE IF NOT EXISTS files(FID INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, tmstp TEXT)')
    conn.commit()
    conn.close()


def checkExistenceFiles(conn):
    c = conn.cursor()
    c.execute('SELECT filename FROM files')
    files_raw = c.fetchall()
    existing = glob.glob(settings.source+'/*.csv')
    files = []
    for x in files_raw:
        files.append(x[0])
    result = []
    for x in existing:
        if len(files) == 0:
            return existing
        else:
            if x not in files:
                result.append(x)
    conn.close()
    return result


def addEntries(files, conn):
    c = conn.cursor()
    for x in files:
        with open(x, "rb") as f:
            print "Importing "+x
            reader = csv.reader(f, delimiter=";")
            fdb = [unicode(x, "utf8"), unicode(date, "utf8")]
            c.execute("INSERT INTO files (filename,tmstp) VALUES(?,?)", fdb)
            c.execute(
                "select FID from files where filename=?", [unicode(x, "utf8")])
            fid = c.fetchone()
            for row in reader:
                to_db = [
                    unicode(row[0], "utf8"), unicode(row[1], "utf8"), fid[0]]
                c.execute(
                    "INSERT INTO data (bedeutung1, bedeutung2, src) VALUES(?, ?, ?)", to_db)
                conn.commit()
                c.execute("select VID from data where bedeutung1=?;", [row[0]])
                vid = c.fetchone()
                c.execute(
                    "INSERT INTO stats (level,anzahl_abfragen, vokabel) VALUES(0,0,?)", vid)
                conn.commit()
    conn.close()


def main():
    print "Vokabel Importer"
    createTables(connectDB(settings.database))
    files = checkExistenceFiles(connectDB(settings.database))
    if len(files) == 0:
        print "[-] Nothing to import."
        sys.exit(0)
    addEntries(files, connectDB(settings.database))
    print "Finished Import"
    sys.exit(0)

if __name__ == "__main__":
    main()
