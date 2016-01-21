#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
from shutil import copyfile
import sys
import csv

def readHerbList():
    herblist = []
    rows = csv.reader(open("./herblist.csv", "rb"))
    for row in rows:
        herblist.append(row[0].strip())
    return herblist

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./symptoms.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def createVector(filepath, filename, herblist, symptom, symptomID):
    rowsize = len(herblist) + 3
    row = [0]*rowsize
    row[0] = filename
    row[1] = "symp"+str(symptomID)

    flagSymp = False
    flagHerb = False
    found_list = []

    src_file = open(filepath+"/"+filename, 'r')
    for line in iter(src_file):
        words = line.split("|")
        for word in words:
            if word == symptom:
                flagSymp = True
                break
        if flagSymp:
            break

    if flagSymp:
        for line in iter(src_file):
            words = line.split("|")
            index = 0
            for word in words:
                if word in herblist:
                    flagHerb = True
                    index = herblist.index(word)
                    found_list.append("h"+str(index))
                    row[index+2] += 1
        if flagHerb:
            row[len(row)-1] = ":".join(found_list)
            index = 0
            for item in row:
                row[index] = str(row[index])
                index += 1
            return row
        else:
            return []
    else:
        return []

def main():
    herblist = readHerbList()
    symptoms = readSymptoms()
    symptomID = 230
    symptom = symptoms[symptomID]

    if len(sys.argv) != 1:
        filedir = sys.argv[1]

        # create path to write output file
        upone_level = path.dirname(filedir.rstrip('/'))
        uptwo_level = path.dirname(upone_level.rstrip('/'))
        dest_path = uptwo_level+"/"+symptom+".csv"

        if isfile(dest_path):
            outfile = open(dest_path, 'a')
        else:
            outfile = open(dest_path, 'w')
            # create CSV Header
            header = ["filename", "symptom"]
            index = 0
            for herb in herblist:
                head = 'h'+str(index)
                header.append(head)
                index += 1
            header.append("founded")

            newline = []
            newline = ",".join(header)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)


        # List all file from target directory
        onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]
        for filename in onlyfiles:
            row = []
            row = createVector(filedir, filename, herblist, symptom, symptomID)
            if len(row) > 0:
                newline = []
                newline = ",".join(row)+"\n"
                outfile.write(newline)

        outfile.close()
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()
