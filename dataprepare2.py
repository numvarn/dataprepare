#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv

def readHerbList():
    herblist = []
    rows = csv.reader(open("./herblist.csv", "rb"))
    for row in rows:
        herblist.append(row[1].strip())
    return herblist

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./symptoms.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main(rootDir, dirname, herblist, symptoms):
    filedir = rootDir+"/"+dirname+"/filtered"
    print "\nProcessing : ", filedir

    # create path to write output file
    destination_dir = rootDir+"/003.feq_matrix"

    # Create directory for store result file
    if not path.exists(destination_dir):
        makedirs(destination_dir)

    dest_path = destination_dir+"/matrix.csv"
    if isfile(dest_path):
        outfile = open(dest_path, 'a')
    else:
        outfile = open(dest_path, 'w')
        # create CSV Header
        header = ["filename"]
        index = 0
        for symp in symptoms:
            head = 'symp'+str(index)
            header.append(head)
            index += 1

        index = 0
        for herb in herblist:
            head = 'h'+str(index)
            header.append(head)
            index += 1

        newline = []
        newline = ",".join(header)+"\n"
        newline = newline.encode('utf-8')
        outfile.write(newline)

    # Count keyword in each file
    onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]
    for filename in onlyfiles:
        fname, fext = filename.split(".")
        row = []
        row.append("FID-"+fname)

        # Count Symptoms
        for symptom in symptoms:
            symp_count = 0
            src_file = open(filedir+"/"+filename, 'r')
            for line in iter(src_file):
                words = line.split("|")
                for word in words:
                    if word == symptom:
                        symp_count += 1
            row.append(str(symp_count))

        # Count Herb
        for herb in herblist:
            herb_count = 0
            src_file = open(filedir+"/"+filename, 'r')
            for line in iter(src_file):
                words = line.split("|")
                for word in words:
                    if word == herb:
                        herb_count += 1
            row.append(str(symp_count))

        newline = ",".join(row)+"\n"
        newline = newline.encode('utf-8')
        outfile.write(newline)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Get root path from command line argument
        rootDir = sys.argv[1]

        # Read CSV
        herblist = readHerbList()
        symptoms = readSymptoms()

        onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
        for dirname in onlyDir:
            if dirname != "001.vector" and dirname != "002.filtered-attbs" and dirname != "003.feq_matrix":
                main(rootDir, dirname, herblist, symptoms)
    else:
        print "Please, Enter File Directory"
