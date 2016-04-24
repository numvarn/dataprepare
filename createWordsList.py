#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

def readHerbList():
    herblist = []
    rows = csv.reader(open("./dictionary/herblist-21-04-16.csv", "rb"))
    for row in rows:
        herblist.append(row[1].strip())
    return herblist

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dictionary/symptoms-21-04-16.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main():
    # Read CSV
    herblist = readHerbList()
    symptoms = readSymptoms()

    wordsSymp = [0] * (len(symptoms) + 1)
    wordHerb = [0] * (len(herblist) + 1)

    wordsSymp[0] = ["Symptoms", "Code", "Total Occurences", "Document Occurences", "Total Occurences(%)", "Document Occurences(%)"]
    wordHerb[0] = ["Herbs", "Code", "Total Occurences", "Document Occurences", "Total Occurences(%)", "Document Occurences(%)"]

    index = 0
    for row in wordsSymp:
        if index > 0:
            wordsSymp[index] = [0, 0, 0, 0, 0, 0]
        index += 1

    index = 0
    for row in wordHerb:
        if index > 0:
            wordHerb[index] = [0, 0, 0, 0, 0, 0]
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

    row_size = len(symptoms) + len(herblist) + 2
    row_count = 1
    rows = csv.reader(open("/Users/phisan/Desktop/wordsVector.csv"))
    totalDocument = 0
    for row in rows:
        if row_count > 1:
            totalDocument += 1
            column_count = 0
            for item in row:
                if column_count > 1 and column_count <= len(symptoms) + 1:
                    sindex = column_count - 2
                    wordsSymp[sindex+1][2] = int(wordsSymp[sindex+1][2]) + int(row[column_count])
                    if int(row[column_count]) != 0:
                        wordsSymp[sindex+1][3] += 1
                elif column_count >= len(symptoms) and column_count < row_size:
                    h_index = column_count - len(symptoms) - 2
                    wordHerb[h_index+1][2] += int(row[column_count])
                    if int(row[column_count]) != 0:
                        wordHerb[h_index+1][3] += 1
                column_count += 1
        row_count += 1

        print "Processing row #",row_count-1

    feq_total = 0
    row_count = 0
    for row in wordHerb:
        if row_count > 0:
            feq_total += row[2]
        row_count += 1

    feq_total_sym = 0
    row_count = 0
    for row in wordsSymp:
        if row_count > 0:
            feq_total_sym += row[2]
        row_count += 1

    row_count = 0
    for row in wordHerb:
        if row_count > 0:
            wordHerb[row_count][4] = (float(row[2]) / float(feq_total)) * 100
            wordHerb[row_count][5] = (float(row[3]) / float(totalDocument)) * 100
        row_count += 1

    row_count = 0
    for row in wordsSymp:
        if row_count > 0:
            wordsSymp[row_count][4] = (float(row[2]) / float(feq_total_sym)) * 100
            wordsSymp[row_count][5] = (float(row[3]) / float(totalDocument)) * 100
        row_count += 1

    # Write result to CSV
    rootPath = "/Users/phisan/Desktop"
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



