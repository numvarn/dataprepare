#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import math

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dictionary/symptoms-21-04-16.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main():
    # Read CSV
    symptoms = readSymptoms()

    wordsSymp = [0] * (len(symptoms) + 1)

    wordsSymp[0] = ["Symptoms", "Code", "Total Occurences", "Document Occurences", "Total Occurences(%)", "Document Occurences(%)", "IDF"]

    index = 0
    for row in wordsSymp:
        if index > 0:
            wordsSymp[index] = [0, 0, 0, 0, 0, 0, 0]
        index += 1

    index = 1
    for symp in symptoms:
        wordsSymp[index][0] = symp
        wordsSymp[index][1] = 's'+str(index-1)
        index += 1

    row_size = len(symptoms) + 3
    row_count = 1

    filename = "336-ถั่วเหลือง.csv"
    rows = csv.reader(open("/Users/phisan/Desktop/006.WordVectorHerb/"+filename))

    totalDocument = 0
    for row in rows:
        if row_count > 1:
            totalDocument += 1
            column_count = 0
            for item in row:
                if column_count > 2 and column_count <= len(symptoms) + 1:
                    sindex = column_count - 3
                    wordsSymp[sindex+1][2] += + int(row[column_count])
                    if int(row[column_count]) != 0:
                        wordsSymp[sindex+1][3] += 1
                column_count += 1
        row_count += 1

        # print "Processing row #",row_count-1

    feq_total_sym = 0
    row_count = 0
    for row in wordsSymp:
        if row_count > 0:
            feq_total_sym += row[2]
        row_count += 1

    row_count = 0
    for row in wordsSymp:
        if row_count > 0:
            wordsSymp[row_count][4] = (float(row[2]) / float(feq_total_sym)) * 100
            wordsSymp[row_count][5] = (float(row[3]) / float(totalDocument)) * 100
            if wordsSymp[row_count][2] != 0:
                wordsSymp[row_count][6] = math.log10(totalDocument / wordsSymp[row_count][3])
        row_count += 1

    print "Total Documents : ", totalDocument

    # Write result to CSV
    rootPath = "/Users/phisan/Desktop"
    destPath = rootPath+"/wordsSymp.csv"
    with open(destPath, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(wordsSymp)

    # Calculate TF-IDF for each term
    destPath = "/Users/phisan/Desktop/"+filename
    outfile = open(destPath, 'w')

    rows = csv.reader(open("/Users/phisan/Desktop/006.WordVectorHerb/"+filename))
    row_count = 0
    new_row = []
    for row in rows:
        column_index = 0
        if row_count > 0:
            for term_feq in row:
                wordList_index = column_index - 2
                if 2 < column_index < len(symptoms) + 3:
                    term_idf = wordsSymp[wordList_index][6]
                    weight = float(term_feq) * float(term_idf)
                    new_row.append(str(weight))
                else:
                    new_row.append(term_feq)

                newline = ",".join(new_row)+"\n"
                newline = newline.encode('utf-8')
                outfile.write(newline)

                column_index += 1
        else:
            for header in row: new_row.append(header)
            newline = ",".join(new_row)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)

        row_count += 1

    outfile.close()


if __name__ == '__main__':
    main()



