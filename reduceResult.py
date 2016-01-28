#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv

def reduceResult(resultFile, symptomsID):
    rows = csv.reader(open(resultFile, "rb"))
    rowNumber = 0
    herblist = []
    for row in rows:
        if rowNumber > 0:
            value = 0
            for index in xrange(2, len(herblist)-1):
                value = int(row[index])
                herblist[index - 2] += value
        else:
            herblist = [0] * (len(row) - 3)
        rowNumber += 1

    # write new csv file
    inputPath = path.dirname(resultFile.rstrip('/'))
    destPath = inputPath+"/"+symptomsID+"-filtered.csv"
    outfile = open(destPath, 'w')

    rows = csv.reader(open(resultFile, "rb"))
    for row in rows:
        newrow = []
        newrow.append(row[0])
        newrow.append(row[1])

        for index in xrange(2, len(herblist)-1):
            if herblist[index - 2] >= (0.2 * rowNumber):
                newrow.append(row[index])
        newrow.append(row[len(row)-1])
        newline = ",".join(newrow)+"\n"
        newline = newline.encode('utf-8')
        outfile.write(newline)

    outfile.close()

def main():
    if len(sys.argv) == 3:
        resultFile = sys.argv[1]+"/"+sys.argv[2]+".csv"
        symptomsID = sys.argv[2]
        reduceResult(resultFile, symptomsID)
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()
