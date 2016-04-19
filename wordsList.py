#!/usr/bin/python
# -*- coding: utf-8 -*-
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

def main():
    # Read CSV
    herblist = readHerbList()
    symptoms = readSymptoms()

    wordsSymp = [0] * (len(symptoms) + 1)
    wordHerb = [0] * (len(herblist) + 1)

    wordsSymp[0] = ["Symptoms", "Code", "Total Occurences", "Document Occurences"]
    wordHerb[0] = ["Herbs", "Code", "Total Occurences", "Document Occurences"]

    index = 0
    for row in wordsSymp:
        if index > 0:
            wordsSymp[index] = [0, 0, 0, 0]
        index += 1

    index = 0
    for row in wordHerb:
        if index > 0:
            wordHerb[index] = [0, 0, 0, 0]
        index += 1

    index = 1
    for symp in symptoms:
        wordsSymp[index][0] = symp
        wordsSymp[index][1] = 's'+str(index-1)
        index += 1

    index = 1
    for herb in herblist:
        wordHerb[index][0] = herb
        wordHerb[index][1] = 'h'+str(index-1)
        index += 1

    row_size = len(symptoms) + len(herblist) + 1
    row_count = 1
    rows = csv.reader(open("/Users/phisanshukkhi/Desktop/matrix.csv"))
    for row in rows:
        if row_count > 1:
            column_count = 0
            for item in row:
                if column_count > 0 and column_count < len(symptoms)+1:
                    wordsSymp[column_count][2] += int(row[column_count])
                    if int(row[column_count]) != 0:
                        wordsSymp[column_count][3] += 1
                elif column_count > 0 and column_count >= len(symptoms) and column_count < row_size:
                    h_index = column_count - len(symptoms)
                    wordHerb[h_index][2] += int(row[column_count])
                    if int(row[column_count]) != 0:
                        wordHerb[h_index][3] += 1
                column_count += 1
        row_count += 1

        print "Processing row #",row_count

    # Write result to CSV
    rootPath = "/Users/phisanshukkhi/Desktop"
    destPath = rootPath+"/wordsSymp.csv"
    with open(destPath, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(wordsSymp)

    destPath = rootPath+"/wordsHerbs.csv"
    with open(destPath, "wb") as fh:
        writer_h = csv.writer(fh)
        writer_h.writerows(wordHerb)

if __name__ == '__main__':
    main()



